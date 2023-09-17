from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from django.conf import settings

# from django.contrib.auth import get_user_model
from django.utils import timezone

from ecommerce.apps.users.models import User
from ecommerce.apps.users.tasks import send_otp

# User = get_user_model()


@pytest.fixture
def user():
    # Create a user with a phone number for testing
    return User.objects.create(
        email="test@example.com",
        password="testpassword",
        phone_number="+254799757242",
    )


@patch("ecommerce.apps.users.tasks.Client")
@pytest.mark.django_db
def test_send_otp_success(mock_twilio_client):
    # Mock Twilio client and message creation
    mock_message = Mock()
    mock_twilio_client.return_value.messages.create.return_value = mock_message

    # Create a user with phone number
    user = User.objects.create(
        email="test@example.com",
        password="testpassword",
        phone_number="+254799757242",
    )

    # valid OTP and expiration time
    otp = 1234
    expiration_time = timezone.now() + timedelta(minutes=10)

    # Call the send_otp task
    send_otp(user.id, otp, expiration_time)

    # Verify that Twilio client was initialized with correct settings
    mock_twilio_client.assert_called_once_with(
        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
    )


@patch("twilio.rest.Client")
@pytest.mark.django_db
def test_send_otp_expired(mock_twilio_client, user):
    # Mock Twilio client and message creation
    mock_message = Mock()
    mock_twilio_client.return_value.messages.create.return_value = mock_message

    # Set an expired OTP expiration time
    otp = 1234
    expiration_time = timezone.now() - timedelta(minutes=10)

    # Call the send_otp task
    send_otp(user.id, otp, expiration_time)

    # Verify that Twilio client was not initialized
    mock_twilio_client.assert_not_called()

    # Verify that the Twilio message was not sent
    mock_message.create.assert_not_called()


@patch("twilio.rest.Client")
@pytest.mark.django_db
def test_send_otp_user_not_found(mock_twilio_client):
    # Mock Twilio client and message creation
    mock_message = Mock()
    mock_twilio_client.return_value.messages.create.return_value = mock_message

    # Set a valid OTP and expiration time
    otp = 1234
    expiration_time = timezone.now() + timedelta(minutes=10)

    # Call the send_otp task with a non-existent user ID
    send_otp(999, otp, expiration_time)

    # Verify that Twilio client was not initialized
    mock_twilio_client.assert_not_called()

    # Verify that the Twilio message was not sent
    mock_message.create.assert_not_called()
