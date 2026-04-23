from django.contrib import admin
from .models import TestRequest, TestType


@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'normal_range', 'price')
    search_fields = ('name',)


@admin.register(TestRequest)
class TestRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test_type', 'status', 'assigned_to', 'requested_at', 'completed_at')
    list_filter = ('status', 'test_type')
    search_fields = ('patient__full_name', 'patient__patient_number', 'test_type__name')
