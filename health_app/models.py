from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.email

class MedicalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    disease =  models.CharField(max_length=200, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    genotype = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    health_worker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='health_worker')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient')
    date = models.DateTimeField()
    status = models.CharField(max_length=10, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('health_worker', 'Health Worker'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
