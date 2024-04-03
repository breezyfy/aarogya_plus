from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from app.models import Patient
from app.models import Doctor
from django.contrib.auth.models import User,Group
from django.contrib import messages
from django.contrib.auth import authenticate,login 
from main_app import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from app.models import Appointment
from .decorators import allowed_users, admin_only
from django.contrib.auth.decorators import login_required





def BASE(request):
    return render(request,'base.html')

def MAIN(request):
    return render(request,'main.html')


def ADD_PATIENT(request):
    if request.method == "POST":
        
        patient_name = request.POST.get('patient_name')
        dob =  request.POST.get('dob')
        age =  request.POST.get('age')
        phone =  request.POST.get('phone')
        gender =  request.POST.get('gender')
        email =  request.POST.get('email')
        address =  request.POST.get('address')

        patient = Patient(
            
            patient_name = patient_name,
            date_of_birth = dob,
            age = age,
            phone = phone,
            gender = gender,
            email = email,
            address = address,
        )
        patient.save()
  

    return render(request,'patients/add_patient.html')

@allowed_users(allowed_roles=['admins'])
def Patient_info(request):
    patients = Patient.objects.all()
    return render(request,'patients/patient_list.html',{'patients': patients})

@allowed_users(allowed_roles=['admins'])
def ADD_DOCTOR(request):
    if request.method == "POST":

        doctor_name = request.POST.get('doctor_name')
        exp = request.POST.get('exp')
        specs = request.POST.get('specs')
        dob =  request.POST.get('dob')
        age =  request.POST.get('age')
        phone =  request.POST.get('phone')
        gender =  request.POST.get('gender')
        email =  request.POST.get('email')

        doctor = Doctor(
            doctor_name = doctor_name,
            exp=exp,
            specs=specs,
            dob = dob,
            age = age,
            phone = phone,
            gender = gender,
            email = email,
            
        )
        doctor.save()
    
    return render(request,'doctors/add_doctor.html')

@allowed_users(allowed_roles=['admins'])
def Doctor_info(request):
    doctors = Doctor.objects.all()
    return render(request,'doctors/doctor_list.html',{'doctors': doctors})


def ADD_APT(request):
    if request.method == "POST":

        doc_name = request.POST.get('doc_name')
        dept = request.POST.get('dept')
        apt_date = request.POST.get('apt_date')
        time_slot = request.POST.get('time_slot')
        problem = request.POST.get('problem')

        appointment = Appointment(
            doc_name = doc_name,
            dept=dept,
            apt_date=apt_date,
            time_slot=time_slot,
            problem=problem
        )
        appointment.save()
    
    return render(request,'appointments/add_appointment.html')

@allowed_users(allowed_roles=['admins'])
def Appointment_info(request):
    appointment = Appointment.objects.all()
    return render(request,'appointments/appointment_list.html',{'appointment': appointment})

@login_required(login_url='login.html')
@admin_only
def DASH(request):
    return render(request,'dashboard.html')

def Login(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user= authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return render(request, "dashboard.html")
        

    return render(request,'login.html')
    



def signup(request):

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exists...Try again!!!")
            return redirect('signup')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email Already Exists...Try again!!!")
            return redirect('signup')
        
        if pass1 != pass2:
            messages.error(request,"Passwords didn't match...Retry!!!")

        group= Group.objects.get_or_create(name='customer')[0]
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name= fname
        myuser.last_name= lname
        myuser.is_active = False
        myuser.groups.add(group)
        myuser.save()

        messages.success(request,"Your Account is created succesfully!!")

        #Email vala part 

        subject = 'Welcome to AarogyaPlus !!!'
        message = 'Hello '+ myuser.first_name +'!! \n' + 'Welcome to AarogyaPlus Community !! \n Thankyou for visiting our Website \n We have sent you an confirmation email, Please confirm using the link to activate your Account'
        from_email = 'aarogya.helpdesk@gmail.com'
        recipient_list =[myuser.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        #Activation Email part

        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ AarogyaPlus helpdesk!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('login')

    
    return render(request,'signup.html')

def activate(request, uidb64,token):
    try:
        uid= force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError, ValueError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        return redirect('login')
    else:
        return render(request, 'activation_failed.html')

