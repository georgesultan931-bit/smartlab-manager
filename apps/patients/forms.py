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
            'gender': forms.Select(
                attrs={'class': 'form-select'},
                choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
            ),
            'date_of_birth': DateInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    # CUSTOM VALIDATION
    def clean_patient_number(self):
        patient_number = self.cleaned_data.get('patient_number')

        # Check if exists (exclude current instance when editing)
        if Patient.objects.filter(patient_number=patient_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A patient with this number already exists.")

        return patient_number

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone:
            # remove spaces
            phone = phone.strip()

            # basic validation
            if not phone.isdigit():
                raise forms.ValidationError("Phone number must contain only digits.")

        return phone