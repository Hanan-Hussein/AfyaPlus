from django.shortcuts import render

def home(request):
    return render(request,'base.html')

def patientprofile(request):
    return render(request,'patient_profile.html')
