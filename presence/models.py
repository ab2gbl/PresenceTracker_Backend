from django.db import models
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


class Company(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.name} ({self.owner.username if self.owner else 'No Owner'})"


class Employee(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    position = models.CharField(max_length=50, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

class AttendanceRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    is_present = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date']

