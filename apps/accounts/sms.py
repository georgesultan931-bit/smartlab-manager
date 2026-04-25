import os
import africastalking
from django.conf import settings


def send_sms(phone, message):
    username = getattr(settings, "AT_USERNAME", "sandbox")
    api_key = getattr(settings, "AT_API_KEY", "")

    if not api_key:
        print("SMS error: AT_API_KEY is missing. Check your .env/settings.py")
        return

    africastalking.initialize(username, api_key)
    sms = africastalking.SMS

    try:
        response = sms.send(message, [phone])
        print("SMS sent:", response)
    except Exception as e:
        print("SMS error:", str(e))