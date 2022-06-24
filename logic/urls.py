from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name= "home"),
    path('patientprofile', views.patientprofile, name= "patientprofile"),
    path('appointment',views.appointment, name= "appointment"),
    path('add-doctor',views.register_doctor, name= "new_doc"),
    path('login',views.login_request , name= "login"),
    path('register',views.register_request , name= "register"),
    path('all_doctors',views.all_doctors,name="doctors")

]


    # path('new/doctor',views.new_doctor, name='new-doctor'),
    # configured the URL
    # path('',views.index, name="homepage")
    
    # path('/',views.patientprofile, name="patientprofile")


