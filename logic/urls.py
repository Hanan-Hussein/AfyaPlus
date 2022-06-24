from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('patientprofile', views.patientprofile, name="patientprofile"),
    path('appointment', views.appointment, name="appointment"),
    path('add-doctor', views.register_doctor, name="new_doc"),
    path('login', views.login_request, name="login"),
    path('register', views.register_request, name="register"),
    path('register_patients_byadmin',
         views.register_patients_byadmin, name="patient_reg"),
    path('all_doctors', views.all_doctors, name="doctors"),
    path('all_patients', views.all_patients, name="patients"),
    path('all_admin', views.all_admin, name="admins"),
    path('reg_admin', views.register_admin, name="reg_admins"),
    path('logout', views.logout_request, name="logout"),
]
