from django.contrib import admin
from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'patient_number', 'gender', 'phone', 'created_at')
    search_fields = ('full_name', 'patient_number', 'phone')
