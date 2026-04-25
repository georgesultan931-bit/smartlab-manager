from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('lab_tech', 'Lab Technician'),
        ('receptionist', 'Receptionist'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='receptionist')
    phone = models.CharField(max_length=20, blank=True, null=True)

    # OTP FIELDS
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    phone_verified = models.BooleanField(default=False)

    def generate_otp(self):
        code = str(random.randint(100000, 999999))
        self.otp_code = code
        self.otp_created_at = timezone.now()
        self.save(update_fields=['otp_code', 'otp_created_at'])
        return code

    def verify_otp(self, code):
        if self.otp_code != code:
            return False

        # expire after 5 minutes
        if timezone.now() > self.otp_created_at + timezone.timedelta(minutes=5):
            return False

        self.phone_verified = True
        self.otp_code = None
        self.save(update_fields=['phone_verified', 'otp_code'])
        return True

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"