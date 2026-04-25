from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .sms import send_sms


def login_view(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/dashboard/")

        return render(request, "accounts/plain_login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "accounts/plain_login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("/accounts/login/")


@login_required
def send_otp(request):
    user = request.user

    if not user.phone:
        messages.error(request, "No phone number found. Please add a phone number first.")
        return redirect("/dashboard/")

    if user.phone_verified:
        messages.info(request, "Phone number is already verified.")
        return redirect("/dashboard/")

    code = user.generate_otp()

    message = f"Your SmartLab OTP is {code}"
    send_sms(user.phone, message)

    print(f"TEST OTP for {user.phone}: {code}", flush=True)

    messages.success(request, "OTP generated. Check VS Code terminal for the test OTP.")
    return redirect("/accounts/verify/")


@login_required
def verify_otp(request):
    user = request.user

    if request.method == "POST":
        code = request.POST.get("otp", "").strip()

        if user.verify_otp(code):
            messages.success(request, "Phone verified successfully.")
            return redirect("/dashboard/")

        messages.error(request, "Invalid or expired OTP.")

    return render(request, "accounts/verify_otp.html")