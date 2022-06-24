from datetime import date
from mimetypes import init
import re
from django.shortcuts import render, redirect
from .forms import doctorsForm, AppointmentsForm, Registration, LoginForm
from django.contrib import messages
from .models import Profile, Appointments
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .email import send_welcome_email
from django.db.models import Q


def index(request):

    return render(request, 'doctors.html')


def new_doctor(request):
    if request.method == "POST":
        form = doctorsForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.name = request.user
            doctor.save()

        return redirect('home')

    else:
        form = doctorsForm()

    return render(request, 'new_doctor.html', {"form": form})


# def doctor(request):
#     profile=Profile.objects.get(user=request.user.id)
#     all_doctors = doctors.objects.get()

#     return render(request,'doctors.html',{"doctors":all_doctors})
@login_required
def home(request):
    doctors = str(Profile.objects.all().filter(type_of_user='DOCTOR').count())
    patients = str(Profile.objects.all().filter(
        type_of_user='PATIENT').count())
    appointments = str(Appointments.objects.all().count())
    is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN') | Q(
        type_of_user='DOCTOR')).filter(user=request.user)
    is_admin = Profile.objects.all().filter(
        type_of_user='ADMIN').filter(user=request.user)
    context = {
        "doctors": doctors,
        "patients": patients,
        "appointments": appointments,
        "is_staff": is_staff,
        "is_admin": is_admin

    }
    return render(request, 'landing.html', context=context)


def patientprofile(request):
    return render(request, 'patient_profile.html')


def appointment(request):
    form = AppointmentsForm()
    form.fields['patient'].initial = request.user
    is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN') | Q(
        type_of_user='DOCTOR')).filter(user=request.user)
    is_admin = Profile.objects.all().filter(
        type_of_user='ADMIN').filter(user=request.user)

    if request.method == 'POST':
        form = AppointmentsForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data["patient"]
            date_appointment = form.cleaned_data["date_appointment"]
            symptoms=form.cleaned_data["symptoms"]
            doctor =form.cleaned_data["doctor"]
            print(patient,date_appointment,symptoms,doctor)
            Appointments.objects.create(users = request.user,date_appointment=date_appointment,symptoms=symptoms,doctor=doctor)
            return redirect('home')
    context = {
        'form': form,
        'is_staff': is_staff,
        'is_admin': is_admin,
        'current_user': request.user
    }
    return render(request, 'appointment.html', context=context)


def register_request(request):
    # is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN')|Q(type_of_user='DOCTOR')).filter(user=request.user)
    # is_admin=Profile.objects.all().filter(type_of_user='ADMIN').filter(user=request.user)

    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful, Please Login")
            return redirect("login")
        messages.error(
            request, "Unsuccessful registration.Please ensure you have entered a strong password and valid email")
    form = Registration()
    context = {"register_form": form,
            #    'is_staff': is_staff,
            #    'is_admin': is_admin
               }
    return render(request, template_name="auth/register.html",context=context)


@login_required
def register_doctor(request):
    is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN') | Q(
        type_of_user='DOCTOR')).filter(user=request.user)
    is_admin = Profile.objects.all().filter(
        type_of_user='ADMIN').filter(user=request.user)

    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            print(request.user)
            # new_profile = Profile(user=request.user,type_of_user='DOCTOR')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            send_welcome_email(request.user.username, password, email)
            form.save()
            new_profile = Profile.objects.update_or_create(
                user__email=email,
                defaults={
                    'type_of_user': 'DOCTOR'
                }
            )

            messages.success(request, "Registration successful, Please Login")
            return redirect("doctors")
        messages.error(
            request, "Unsuccessful registration.Please ensure you have entered a strong password and valid email")
    form = Registration()
    return render(request, template_name="auth/doctor_register.html", context={"register_form": form, 'is_staff': is_staff,
                                                                               'is_admin': is_admin})


@login_required
def register_patients_byadmin(request):
    is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN') | Q(
        type_of_user='DOCTOR')).filter(user=request.user)
    is_admin = Profile.objects.all().filter(
        type_of_user='ADMIN').filter(user=request.user)

    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            # new_profile = Profile(user=request.user,type_of_user='DOCTOR')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            send_welcome_email(request.user.username, password, email)
            form.save()
            messages.success(request, "Registration successful, Please Login")
            return redirect("patients")
        messages.error(
            request, "Unsuccessful registration.Please ensure you have entered a strong password and valid email")
    form = Registration()
    return render(request, template_name="auth/patient_b2b.html", context={"register_form": form, 'is_staff': is_staff,
                                                                           'is_admin': is_admin})


def login_request(request):
    # is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN')|Q(type_of_user='DOCTOR')).filter(user=request.user)
    # is_admin=Profile.objects.all().filter(type_of_user='ADMIN').filter(user=request.user)

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('home')
    form = LoginForm()
    context = {
        "form": form,
        # 'is_staff':is_staff,
        # 'is_admin':is_admin
    }
    return render(request, 'auth/login.html', context=context)


@login_required
def all_doctors(request):
    is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN') | Q(
        type_of_user='DOCTOR')).filter(user=request.user)
    is_admin = Profile.objects.all().filter(
        type_of_user='ADMIN').filter(user=request.user)

    doctors = Profile.objects.all().filter(type_of_user='DOCTOR')
    context = {
        "doctors": doctors,
        'is_staff': is_staff,
        'is_admin': is_admin
    }
    return render(request, 'all_doctors.html', context=context,)


@login_required
def all_patients(request):
    is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN') | Q(
        type_of_user='DOCTOR')).filter(user=request.user)
    is_admin = Profile.objects.all().filter(
        type_of_user='ADMIN').filter(user=request.user)

    patients = Profile.objects.all().filter(type_of_user='PATIENT')
    context = {
        "patients": patients,
        'is_staff': is_staff,
        'is_admin': is_admin
    }
    return render(request, 'all_patients.html', context=context)


def all_admin(request):
    is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN') | Q(
        type_of_user='DOCTOR')).filter(user=request.user)
    is_admin = Profile.objects.all().filter(
        type_of_user='ADMIN').filter(user=request.user)

    admins = Profile.objects.all().filter(type_of_user='ADMIN')
    context = {
        "admins": admins,
        'is_staff': is_staff,
        'is_admin': is_admin
    }
    return render(request, 'all_admin.html', context=context)


@login_required
def register_admin(request):
    is_staff = Profile.objects.all().filter(Q(type_of_user='ADMIN') | Q(
        type_of_user='DOCTOR')).filter(user=request.user)
    is_admin = Profile.objects.all().filter(
        type_of_user='ADMIN').filter(user=request.user)

    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            # new_profile = Profile(user=request.user,type_of_user='DOCTOR')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            send_welcome_email(request.user.username, password, email)
            form.save()
            new_profile = Profile.objects.update_or_create(
                user__email=email,
                defaults={
                    'type_of_user': 'ADMIN'
                }
            )

            messages.success(request, "Registration successful")
            return redirect("admins")
        messages.error(
            request, "Unsuccessful registration.Please ensure you have entered a strong password and valid email")
    form = Registration()
    return render(request, template_name="auth/doctor_register.html", context={"register_form": form, 'is_staff': is_staff,
                                                                               'is_admin': is_admin})

def logout_request(request):
    logout(request)
    return redirect('login')
