from django.db import models


class Patient(models.Model):
    full_name = models.CharField(max_length=150)
    patient_number = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.full_name} - {self.patient_number}'
