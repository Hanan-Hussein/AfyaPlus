from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= "home"),
    # path('patientprofile', views.patientprofile, name= "patientprofile"),
    path('new/doctor',views.new_doctor, name='new-doctor'),
    path('appointment',views.appointment, name= "appointment"),
    path('login',views.login_request , name= "login"),
    path('register',views.register_request , name= "register"),

]


    # path('new/doctor',views.new_doctor, name='new-doctor'),
    # configured the URL
    # path('',views.index, name="homepage")
    
    # path('/',views.patientprofile, name="patientprofile")


