import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from . import models


class CustomUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # get jwt token
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            # decode token
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token has expired")
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("Token is invalid")

        user = models.User.objects.filter(id=payload["id"]).first()

        return (user, None)
