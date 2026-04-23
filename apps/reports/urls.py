from django.urls import path
from .views import generate_report

app_name = "reports"

urlpatterns = [
    path("<int:pk>/", generate_report, name="generate_report"),
]