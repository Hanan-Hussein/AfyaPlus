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

class Registration(UserCreationForm):
    email = forms.EmailField(
	    required=True, widget=forms.EmailInput(attrs={'class': 'my-2 input-val bg-transparent'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(Registration, self).__init__(*args, **kwargs)
        self.fields['password2'].widget.attrs['class'] = 'input-val bg-transparent my-2'
        self.fields['username'].widget.attrs['class'] = 'input-val bg-transparent my-2'
        self.fields['password1'].widget.attrs['class'] = 'input-val bg-transparent my-2'

    def save(self, commit=True):
        user = super(Registration, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LoginForm(forms.ModelForm):

    username = forms.CharField(max_length=80)
    password = forms.CharField(widget=forms.PasswordInput())
    # required_css_class = 'required d-none'
    username.widget.attrs.update(
        {'class': 'form-control input-val bg-transparent my-2' })
    password.widget.attrs.update(
        {'class': 'form-control  input-val bg-transparent my-2'})

    class Meta:
        model = Profile
        fields = ('username', 'password')
