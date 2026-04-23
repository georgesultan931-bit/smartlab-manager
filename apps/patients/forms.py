from django import forms
from .models import Patient


class DateInput(forms.DateInput):
    input_type = 'date'


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'patient_number', 'gender', 'date_of_birth', 'phone', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patient_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'date_of_birth': DateInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
