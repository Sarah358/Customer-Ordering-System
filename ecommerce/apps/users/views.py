from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from . import authentication
from . import serializers as user_serializer
from . import services


class UserViewSet(viewsets.ViewSet):
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        user = request.user
        serializer = user_serializer.UserSerializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        resp = Response({"message": "You have successfully logged out"})
        resp.delete_cookie("jwt")
        return resp


class AuthViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        serializer.instance = services.create_user(user_dc=data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = services.user_email_selector(email=email)

        if user is None or not user.check_password(raw_password=password):
            return Response({"detail": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token = services.create_token(user_id=user.id)
        resp = Response()
        resp.set_cookie(key="jwt", value=token, httponly=True)
        return resp
