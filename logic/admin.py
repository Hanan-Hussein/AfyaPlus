from django.contrib import admin

from logic.models import Profile, doctors,Appointments

# Register your models here.
admin.site.register(Profile)
admin.site.register(Appointments)

admin.site.register(doctors)
