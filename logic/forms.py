from django import forms
from .models import Appointments,Profile
from django.forms.widgets import DateInput


class AppointmentsForm(forms.ModelForm):
    patient = forms.CharField(max_length=100)
    patient.widget.attrs.update({'class': 'form-control','readonly': True,'value':'Jaffar Hussein'})
    doctors = Profile.objects.filter(type_of_user = 'DOCTOR')
    for doc in doctors:
        
        doctors = [
        ('doc', 'doc'),
        ('green', 'doc'),
        ('doc', 'doc'),
    ]

    # doctor = forms.ChoiceField(choices=doctors)
    doctor = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=doctors,
    )

    class Meta:
        model = Appointments
        fields = ("date_appointment", "symptoms")
    def __init__(self, *args, **kwargs):
        super(AppointmentsForm, self).__init__(*args, **kwargs)
        self.fields['date_appointment'].widget = DateInput(attrs={'class': 'form-control','type': 'date'})
        self.fields['symptoms'].widget.attrs.update({'class': 'form-control','rows':'5' })
        
    field_order = ['patient', 'date_appointment', 'symptoms','doctor']
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import doctors


class doctorsForm(forms.ModelForm):
    class Meta:
        model=doctors
        fields = ['user','specialization_area','bio','phone','email']
