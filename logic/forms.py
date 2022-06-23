from django.contrib.auth.forms import UserCreationForm
from .models import doctors
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from .models import Appointments, Profile
from django.forms.widgets import DateInput


class AppointmentsForm(forms.ModelForm):
    patient = forms.CharField(max_length=100)
    patient.widget.attrs.update(
        {'class': 'form-control', 'readonly': True, 'value': 'Jaffar Hussein'})

    class Meta:
        model = Appointments
        fields = ("doctor", "date_appointment", "symptoms")

    def __init__(self, *args, **kwargs):
        super(AppointmentsForm, self).__init__(*args, **kwargs)
        self.fields['date_appointment'].widget = DateInput(
            attrs={'class': 'form-control', 'type': 'date'})
        self.fields['symptoms'].widget.attrs.update(
            {'class': 'form-control', 'rows': '5'})
        self.fields['doctor'].widget.attrs.update(
             {'class': 'form-select'})

    field_order = ['patient', 'date_appointment', 'symptoms', 'doctor']


class doctorsForm(forms.ModelForm):
    class Meta:
        model = doctors
        fields = ['specialization_area', 'bio', 'phone', 'email']
