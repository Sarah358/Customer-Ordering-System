# tasks.py
from celery import shared_task
from django.conf import settings
from twilio.rest import Client

from .models import Order


@shared_task
def send_order_confirmation_sms(order_id):
    order = Order.objects.get(id=order_id)
    buyer_phone = str(order.buyer.profile.phone_number)

    # Initialize the Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Message
    message = f"Thank you for your order with us! Your order reference code is {order.ref}. Total cost: {order.total_cost}"

    # Send the SMS using Twilio
    response = client.messages.create(
        body=message, from_=settings.TWILIO_PHONE_NUMBER, to=buyer_phone
    )

    if response.status == "queued":
        # SMS sent successfully
        pass
    else:
        # Handle the case where SMS sending failed
        pass
