from django.shortcuts import render, redirect
from .forms import doctorsForm, AppointmentsForm, Registration, LoginForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .email import send_welcome_email


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
def home(request):
    doctors=str(Profile.objects.all().filter(type_of_user='DOCTOR').count())
    context = {
        "doctors":doctors

    }
    return render(request, 'landing.html', context=context)


def patientprofile(request):
    return render(request, 'patient_profile.html')


def appointment(request):
    form = AppointmentsForm()
    if request.method == 'POST':
        form = AppointmentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form,
    }
    return render(request, 'appointment.html', context=context)


def register_request(request):
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful, Please Login")
            return redirect("login")
        messages.error(
            request, "Unsuccessful registration.Please ensure you have entered a strong password and valid email")
    form = Registration()
    return render(request, template_name="auth/register.html", context={"register_form": form})


@login_required
def register_doctor(request):
    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            print(request.user)
            # new_profile = Profile(user=request.user,type_of_user='DOCTOR')
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            send_welcome_email(request.user.username,password,email)
            form.save()
            new_profile = Profile.objects.update_or_create(
                user__email=email,
                defaults={
                    'type_of_user':'DOCTOR'
                }
            )

            messages.success(request, "Registration successful, Please Login")
            return redirect("doctors")
        messages.error(
            request, "Unsuccessful registration.Please ensure you have entered a strong password and valid email")
    form = Registration()
    return render(request, template_name="auth/doctor_register.html", context={"register_form": form})


def login_request(request):
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
    }
    return render(request, 'auth/login.html', context=context)

@login_required
def all_doctors(request):
    doctors=Profile.objects.all().filter(type_of_user='DOCTOR')
    context={
        "doctors": doctors,
    }
    return render(request,'all_doctors.html',context=context)