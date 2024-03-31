"""
URL configuration for main_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base', views.BASE,name='base'),
    path('Patients/add',views.ADD_PATIENT,name='add_patient'),
    path('dashboard',views.DASH, name='dashboard'),
    path('',views.Login,name='login'),
    path('signup',views.signup,name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('Patients/info',views.Patient_info,name='patient_list'),
    path('Doctors/add',views.ADD_DOCTOR,name='add_doctor'),
    path('Doctors/info',views.Doctor_info,name='doctor_list'),
    path('Appointment/add',views.ADD_APT,name='add_appointment'),
    path('Appointment/info',views.Appointment_info,name='appointment_list')
]
