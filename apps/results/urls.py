from django.urls import path
from . import views

urlpatterns = [
    path('', views.result_list, name='list'),
    path('test-request/<int:test_request_id>/save/', views.result_create, name='create'),
    path('<int:pk>/', views.result_detail, name='detail'),
]
