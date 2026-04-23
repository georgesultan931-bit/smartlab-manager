from django.conf import settings
from django.db import models
from apps.tests.models import TestRequest


class Result(models.Model):
    test_request = models.OneToOneField(TestRequest, on_delete=models.CASCADE, related_name='result')
    result_value = models.CharField(max_length=255)
    remarks = models.TextField(blank=True, null=True)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-entered_at']

    def __str__(self):
        return f'Result for {self.test_request}'
