from django.db import models
 

# Create your models here.


class Patient(models.Model):
    p_id = models.AutoField(primary_key=True)
    patient_name =models.CharField( max_length=100)
    date_of_birth =models.DateField( max_length=100)
    age = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=50)
    address = models.TextField() 

    def __str__(self):
     return self.patient_name

class Doctor(models.Model):
    d_id = models.AutoField(primary_key=True)
    doctor_name =models.CharField( max_length=100)
    dob =models.CharField( max_length=100)
    specs =models.CharField(max_length=100)
    exp =models.CharField(max_length=100)
    age = models.IntegerField()
    phone = models.IntegerField()
    email = models.EmailField(max_length=100)
    gender = models.CharField(max_length=50)
     

    def __str__(self):
     return self.doctor_name 
  
class Appointment(models.Model):
   doc =models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='appointments_as_doc')
   pat=models.ForeignKey(Patient,on_delete=models.CASCADE)
   serv= models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='appointments_as_service')
   apt_date=models.CharField( max_length=100)
   apt_id = models.AutoField(primary_key=True)
   time_slot =models.CharField( max_length=100)
   problem =models.TextField()

   def __str__(self):
     return self.pat
   
class Payment(models.Model):
  pay_id=models.AutoField(primary_key=True)
  d=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='appointments_as_d')
  p=models.ForeignKey(Patient,on_delete=models.CASCADE)
  s=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name='appointments_as_s')
  amount = models.IntegerField()
  date = models.DateField()
  services=models.CharField(max_length=100)
  pay_type = models.CharField(max_length=20)
  cardcheck_no=models.CharField(max_length=50)

  def __str__(self):
     return self.p