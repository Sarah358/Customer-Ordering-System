import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
User = get_user_model()


class Profile(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone number"), max_length=30, default="+254799757242"
    )
    profile_photo = models.ImageField(
        verbose_name=_("profile photo"), default="/profile_default.png"
    )
    city = models.CharField(
        verbose_name=_("City"), max_length=180, default="Nairobi", blank=False, null=False
    )
    address = models.CharField(
        verbose_name=_("Address"), max_length=180, default="Roysambu", blank=False, null=False
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
