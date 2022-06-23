from re import A
from django.shortcuts import render
from .forms import AppointmentsForm
from .models import Profile
# Create your views here.

def index(request):
    form = AppointmentsForm()
    if request.method == 'POST':
        if form.is_valid():
            print('x')
            
            form = AppointmentsForm(request.POST)
            print(form.cleaned_data)
    # doctors = list(Profile.objects.filter(type_of_user = 'DOCTOR'))
    # print(doctors)
    context={
        "form": form,
    }
    return render(request, 'index.html',context=context)