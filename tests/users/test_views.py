from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

# from ecommerce.apps.users.models import User

User = get_user_model()


class UserViewSetTestCase(APITestCase):
    def test_user_signup(self):
        data = {
            "username": "john",
            "email": "john@gmail.com",
            "phone_number": "+254799757242",
            "first_name": "john",
            "last_name": "doe",
            "password": "Malaika_1",
            "re_password": "Malaika_1",
        }
        response = self.client.post("/api/v1/users/signup/user_signup/", data, format="json")
        if response.status_code != status.HTTP_201_CREATED:
            print(response.content)  # Add this line to print the response content
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)
        user = User.objects.get(email=data["email"])
        self.assertFalse(user.is_active)  # User should be inactive until OTP verification

    def test_verify_otp(self):
        # Create a user with OTP-related data
        user = User.objects.create(
            email="test@example.com",
            password="testpassword",
            otp=1234,
            otp_expiration=timezone.now() + timedelta(minutes=10),
        )

        # Create a valid OTP verification payload
        data = {"user_id": user.id, "otp": user.otp}

        # Send a POST request to verify OTP
        response = self.client.post("/api/v1/users/signup/verify_otp/", data, format="json")

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the user is active after OTP verification
        user = User.objects.get(id=user.id)
        self.assertTrue(user.is_active)  # User should be active after OTP verification


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            username="testuser",
            first_name="John",
            last_name="Doe",
            phone_number="+254799757242",
            is_active=True,
        )
        self.login_url = "/api/v1/users/login/"
        self.client = APIClient()

    def test_login(self):
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.cookies["token"].value, response.data["token"])

    def test_login_inactive_user(self):
        # Deactivate the user
        self.user.is_active = False
        self.user.save()
        data = {
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue("error" in response.data)

    def test_login_invalid_credentials(self):
        data = {
            "email": "test@example.com",
            "password": "invalidpassword",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue("error" in response.data)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword",
            username="testuser",
            first_name="John",
            last_name="Doe",
            phone_number="+254799757242",
            is_active=True,
        )
        self.client = APIClient()

    def test_logout_success(self):
        # Authenticate the user by creating a token
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        # Logout the user
        response = self.client.post("/api/v1/users/logout/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logged out successfully')

    def test_logout_failure_unauthenticated(self):
        # Try to logout without authentication
        response = self.client.post("/api/v1/users/logout/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
