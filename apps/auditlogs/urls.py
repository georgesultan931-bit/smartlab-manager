from django.urls import path
from .views import auditlog_list

urlpatterns = [
    path('', auditlog_list, name='list'),
]
