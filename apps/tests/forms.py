from django import forms
from apps.accounts.models import User
from .models import TestRequest, TestType


class TestTypeForm(forms.ModelForm):
    class Meta:
        model = TestType
        fields = ['name', 'description', 'normal_range', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'normal_range': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TestRequestForm(forms.ModelForm):
    class Meta:
        model = TestRequest
        fields = ['patient', 'test_type', 'assigned_to', 'status']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'test_type': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(role='lab_tech')
        self.fields['assigned_to'].required = False
