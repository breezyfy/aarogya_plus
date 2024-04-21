from calendar import month
from itertools import count
from time import strftime
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from html5lib import serialize
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
import razorpay
from app.models import Payment
import pandas as pd
from django.db.models.functions import TruncMonth
from django.db.models import Count

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
    doc_name1 = Doctor.objects.all()
    service1 = Doctor.objects.all()
    pat_name1 = Patient.objects.all()
    if request.method == "POST":
        doc = request.POST.get('doc')
        pat = request.POST.get('pat')
        serv = request.POST.get('serv')
        apt_date = request.POST.get('apt_date')
        time_slot = request.POST.get('time_slot')
        problem = request.POST.get('problem')

        # Define the doc variable
        doc = Doctor.objects.get(doctor_name=doc)
        # Get the Patient instance
        pat= Patient.objects.get(patient_name=pat)
        # Get the Service instance
        serv = Doctor.objects.get(specs=serv)
        appointment = Appointment(
            doc=doc,
            pat=pat,
            serv=serv,
            apt_date=apt_date,
            time_slot=time_slot,
            problem=problem,
        )
        # Save the Appointment instance
        appointment.save()

        # Send an email after the appointment is booked
        subject = 'Appointment Confirmation'
        message = f'Hello {pat},\n\nYour appointment with {doc} has been booked for {apt_date} at {time_slot}.\n\nProblem: {problem}\n\nThank you for choosing AarogyaPlus.\n\nBest Regards,\nAarogyaPlus Team'
        from_email = 'aarogya.helpdesk@gmail.com'
        to_email = [pat.email]
        send_mail(subject, message, from_email, to_email, fail_silently=False)


    context={'doc':doc_name1,'pat':pat_name1, 'serv':service1}
    return render(request,'appointments/add_appointment.html',context)
    

@allowed_users(allowed_roles=['admins'])
def Appointment_info(request):
    appointment = Appointment.objects.all()
    return render(request,'appointments/appointment_list.html',{'appointment': appointment})

@login_required(login_url='login.html')
@allowed_users(allowed_roles=['admins'])
def DASH(request):
    doctors=Doctor.objects.all()
    patients=Patient.objects.all()
    appointments=Appointment.objects.all()
    doctorcount=Doctor.objects.count()
    patientcount=Patient.objects.count()
    appcount=Appointment.objects.count()



    mydict={
        'doctors':doctors,
        'patients':patients,
        'appointments':appointments,
        'doctorcount':doctorcount,
        'patientcount':patientcount,
        'appcount':appcount,
    }


    return render(request,'dashboard.html',mydict)

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
    
def ADD_PAYMENT(request):
    doc_name2 = Doctor.objects.all()
    service2 = Doctor.objects.all()
    pat_name2 = Patient.objects.all()
    if request.method == "POST":
        d= request.POST.get('d')
        p= request.POST.get('p')
        s= request.POST.get('s')
        date = request.POST.get('date')
        amount=request.POST.get('amount')
        pay_type= request.POST.get('pay_type')
        cardcheck_no= request.POST.get('cardcheck_no')
        services=request.POST.get('services')

        # Define the doc variable
        d = Doctor.objects.get(doctor_name=d)
        # Get the Patient instance
        p= Patient.objects.get(patient_name=p)
        # Get the Service instance
        s= Doctor.objects.get(specs=s)
        payments = Payment(
            d=d,
            p=p,
            s=s,
            date=date,
            amount=amount,
            pay_type=pay_type,
            cardcheck_no=cardcheck_no,
            services=services,
        )
        # Save the Appointment instance
        payments.save()
        amount = 50000
        currency = 'INR'
        client = razorpay.Client(auth=('rzp_test_2JlOmslRAoND06','60S4UQ0fmzugkpqNskvVlRkZ'))
        payments = client.order.create({'amount':amount,'currency':currency,'payment_capture': '1'})
        
    
    context={'d':doc_name2,'p':pat_name2, 's':service2}
    return render(request,'payments/add_payment.html',context)

#@allowed_users(allowed_roles=['admins'])
def Payment_info(request):
    payments = Payment.objects.all()
    return render(request,'payments/payment_list.html',{'payments': payments})


from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import csv
import xlsxwriter

def patients_report(request, format):
    # Get patient data from the database
    patients = Patient.objects.all()

    # Create a list of lists to store the table data
    table_data = [['Patient Name', 'Date of Birth', 'Age', 'Phone', 'Gender', 'Email', 'Address']]
    for patient in patients:
        table_data.append([patient.patient_name, patient.date_of_birth, patient.age, patient.phone, patient.gender, patient.email, patient.address])

    # Create a PDF response
    if format == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="patients.pdf"'

        # Create a table from the data
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        # Create a PDF document and add the table
        doc = SimpleDocTemplate(response, pagesize=letter)
        doc.build([table])

    # Create a CSV response
    elif format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="patients.csv"'

        # Create a CSV writer and write the table data
        writer = csv.writer(response)
        writer.writerow(['Patient Name', 'Date of Birth', 'Age', 'Phone', 'Gender', 'Email', 'Address'])
        for row in table_data:
            writer.writerow(row)

    # Create an Excel response
    elif format == 'excel':
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="patients.xls"'

        # Create an Excel workbook and worksheet
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()

        # Write the table data to the worksheet
        row = 0
        for col, value in enumerate(['Patient Name', 'Date of Birth', 'Age', 'Phone', 'Gender', 'Email', 'Address']):
            worksheet.write(row, col, value)
        for row, data in enumerate(table_data):
            for col, value in enumerate(data):
                worksheet.write(row + 1, col, value)

        # Close the workbook
        workbook.close()

    return response

def delete_patient(request, p_id):
    patient = get_object_or_404(Patient, id=p_id)
    patient.delete()
    return redirect('patient_list')
