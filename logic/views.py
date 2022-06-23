from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from .models import doctors, Profile
from .forms import doctorsForm
from django.http import JsonResponse
import json

# Create your views here.

def index(request):

     return render(request, 'doctors.html')


def new_doctor(request):
    if request.method=="POST":
        form =doctorsForm(request.POST,request.FILES)
        if form.is_valid():
            doctor = form.save(commit = False)
            doctor.name = request.user
            doctor.save()

        return HttpResponseRedirect('/doctors')

    else:
        form = doctorsForm()

    return render(request,'new_doctor.html',{"form":form})


# def doctor(request):
#     profile=Profile.objects.get(user=request.user.id)
#     all_doctors = doctors.objects.get()

#     return render(request,'doctors.html',{"doctors":all_doctors})