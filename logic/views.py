from django.shortcuts import render, redirect
from .forms import doctorsForm, AppointmentsForm


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
    context = {

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
