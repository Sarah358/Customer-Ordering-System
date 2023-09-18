import json
import random
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateUserSerializer, UserLoginSerializer, VerifyOTPSerializer
from .tasks import send_otp

User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def user_signup(self, request):
        if request.method == 'POST':
            serializer = CreateUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.is_active = False  # Deactivate user until OTP verification

                # Generate a random OTP
                otp = random.randint(1000, 9999)  # Generate a 4-digit OTP (customize as needed)

                # Set the expiration time for the OTP (10 minutes from now)
                expiration_time = timezone.now() + timedelta(minutes=10)

                user.otp = otp
                user.otp_expiration = expiration_time
                user.save()

                # Trigger the background task to send OTP with expiration time
                send_otp.delay(
                    user.id, otp, expiration_time
                )  # Pass the generated OTP and expiration time to the task

                return Response(
                    {
                        "message": "User registered successfully. Please verify your account with OTP.",
                        "user": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            otp_entered = serializer.validated_data['otp']

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

            if user.otp is None or user.otp_expiration is None:
                return Response(
                    {"message": "OTP has not been generated."}, status=status.HTTP_400_BAD_REQUEST
                )

            if user.otp != otp_entered:
                return Response(
                    {"message": "Invalid OTP. Please try again."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            current_time = timezone.now()
            if current_time > user.otp_expiration:
                return Response(
                    {"message": "OTP has expired. Please request a new OTP."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # OTP is valid; activate the user
            user.is_active = True
            user.otp = None
            user.otp_expiration = None
            user.save()

            return Response(
                {"message": "Account verified successfully. You can now log in."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# authenticate user
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_active:  # Check if the user is active
                # Delete the existing token (if any)
                Token.objects.filter(user=user).delete()

                login(request, user)

                # Create a new token with an expiration time
                token, created = Token.objects.get_or_create(user=user)
                token.expires = timezone.now() + timedelta(hours=24)  # Set expiration time
                token.save()

                response = Response({'token': token.key}, status=status.HTTP_200_OK)
                response.set_cookie(key='token', value=token.key, httponly=True)

                return response
            elif user is not None:
                return Response(
                    {'error': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                return Response(
                    {'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the existing token and related cookies
        user = request.user
        Token.objects.filter(user=user).delete()

        # Logout the user
        logout(request)

        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

        # Delete the token cookie
        response.delete_cookie('token')

        return response
