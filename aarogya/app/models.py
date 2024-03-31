from django.db import models
 

# Create your models here.


class Patient(models.Model):
    p_id = models.AutoField(primary_key=True)
    patient_name =models.CharField( max_length=100)
    date_of_birth =models.CharField( max_length=100)
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
   doc_name =models.CharField( max_length=100)
   dept=models.CharField( max_length=100)
   apt_date=models.CharField( max_length=100)
   Apt_no = models.AutoField(primary_key=True)
   time_slot =models.CharField( max_length=100)
   problem =models.TextField()

   def __str__(self):
     return self.doc_name 