from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_request_list, name='list'),
    path('new/', views.test_request_create, name='create'),
    path('<int:pk>/edit/', views.test_request_update, name='update'),
    path('types/', views.test_type_list, name='type_list'),
    path('types/new/', views.test_type_create, name='type_create'),
]
