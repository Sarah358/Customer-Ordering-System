# tasks.py
from celery import shared_task

# from datetime import datetime
from django.conf import settings
from django.utils import timezone
from twilio.rest import Client

from .models import User


@shared_task
def send_otp(user_id, otp, expiration_time):
    try:
        user = User.objects.get(id=user_id)

        # Check if the OTP is still valid
        current_time = timezone.now()
        if current_time <= expiration_time:
            # OTP is still valid, send it via Twilio
            user_phone = str(user.phone_number)

            # Initialize the Twilio client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            message = f"Your OTP for account verification is {otp}"

            # Send the SMS using Twilio
            response = client.messages.create(
                body=message, from_=settings.TWILIO_PHONE_NUMBER, to=user_phone
            )

            if response.status == "queued":
                # OTP sent successfully
                pass
            else:
                # Handle the case where OTP sending failed
                pass

        else:
            # Handle the case where the OTP has expired
            pass

    except User.DoesNotExist:
        # Handle the case where the user doesn't exist
        pass
