from django.contrib import admin
from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('test_request', 'entered_by', 'entered_at', 'updated_at')
    search_fields = ('test_request__patient__full_name', 'test_request__patient__patient_number')
