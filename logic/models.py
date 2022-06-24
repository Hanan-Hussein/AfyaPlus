from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    profilephoto = CloudinaryField("profilephoto")
    user = models.OneToOneField(
        User,  related_name='profiles', on_delete=models.CASCADE)
    specialization = models.CharField(max_length=50, blank=True)

    ADMIN = 'ADMIN'
    DOCTOR = 'DOCTOR'
    PATIENT = 'PATIENT'

    TYPES_OF_USER = [
        (ADMIN, 'ADMIN'),
        (DOCTOR, 'DOCTOR'),
        (PATIENT, 'PATIENT'),

    ]
    type_of_user = models.CharField(
        max_length=20,
        choices=TYPES_OF_USER,
        default=PATIENT,
    )

    def __str__(self):
        return self.user.username

    @classmethod
    def save_profile(cls, profile):
        cls.save(profile)

    @classmethod
    def update_profile(cls, username, email, profilephoto):
        cls.update(username=username, email=email, profilephoto=profilephoto)

    @classmethod
    def delete_profile(cls, profile):
        cls.delete(profile)


class doctors(models.Model):
    user = models.OneToOneField(
        User,  related_name='doctors', on_delete=models.CASCADE)
    specialization_area = models.CharField(max_length=50, blank=True)
    bio = models.CharField(max_length=500)
    email = models.EmailField(default="", blank=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.specialization_area


class Appointments(models.Model):
    date_appointment = models.DateTimeField()
    users = models.ForeignKey(
        User, related_name="users", on_delete=models.CASCADE)
    symptoms = models.TextField()
    doctor = models.ForeignKey(
        User,  related_name='doctors_ap', on_delete=models.CASCADE, null=True)
