import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from ecommerce.apps.profiles.models import Profile
from ecommerce.settings.base import AUTH_USER_MODEL

logger = logging.getLogger(__name__)


# signals to create user profile once a user is created
@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    logger.info(f"{instance}'s profile created")
