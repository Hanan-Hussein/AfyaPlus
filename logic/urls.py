from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= "home"),
    path('patientprofile', views.patientprofile, name= "patientprofile"),
    path('new/doctor/',views.new_doctor, name='new-doctor'),
    path('doctors/',views.doctor, name='doctors'),
    path('appointment',views.appointment, name= "appointment"),
]
