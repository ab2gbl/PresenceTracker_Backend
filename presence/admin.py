from django.contrib import admin
from .models import Company, Employee, AttendanceRecord
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(AttendanceRecord)

