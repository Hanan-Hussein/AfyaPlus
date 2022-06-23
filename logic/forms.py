from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import doctors


class doctorsForm(forms.ModelForm):
    class Meta:
        model=doctors
        fields = ['user','specialization_area','bio','phone','email']