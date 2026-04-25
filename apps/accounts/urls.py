from django.urls import path
from . import views

urlpatterns = [
    # AUTH
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # OTP
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify/', views.verify_otp, name='verify'),
]