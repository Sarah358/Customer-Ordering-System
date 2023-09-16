from datetime import timedelta

import pytest
from django.utils import timezone

from ecommerce.apps.users.models import User


def test_user_str(base_user):
    """Test the custom user model string representation"""
    assert base_user.__str__() == f"{base_user.username}"


def test_user_short_name(base_user):
    """Test that the user models get_short_name method works"""
    short_name = f"{base_user.username}"
    assert base_user.get_short_name() == short_name


def test_user_full_name(base_user):
    """Test that the user get_full_name method works"""
    full_name = f"{base_user.first_name} {base_user.last_name}"
    assert base_user.get_full_name == full_name


def test_base_user_email_is_normalized(base_user):
    """Test that a new users email is normalized"""
    email = base_user.email
    assert base_user.email == email.lower()


def test_super_user_email_is_normalized(super_user):
    """Test that an admin users email is normalized"""
    email = super_user.email
    assert super_user.email == email.lower()


def test_super_user_is_not_staff(user_factory):
    """Test that an error is raised when an admin user has is_staff set to false"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=False)
    assert str(err.value) == "Superuser must have is_staff=True"


def test_super_user_is_not_superuser(user_factory):
    """Test that an error is raised when an admin user has is_superuser set to False"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(err.value) == "Superuser must have is_superuser=True"


def test_create_user_with_no_email(user_factory):
    """Test that creating a new user with no email address raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == "an email address is required"


def test_create_use_with_no_username(user_factory):
    """Test that creating a new user with no usrname raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(username=None)
    assert str(err.value) == "users must provide a username"


def test_create_use_with_no_phone_number(user_factory):
    """Test that creating a new user with no usrname raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(phone_number=None)
    assert str(err.value) == "users must provide a phone_number"


def test_create_user_with_no_firstname(user_factory):
    """Test creating a new user without a firstname raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == "users must provide a first name"


def test_create_user_with_no_lastname(user_factory):
    """Test creating a new user without a lastname raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == "users must provide a last name"


def test_create_superuser_with_no_email(user_factory):
    """Test creating a superuser without an email address raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "an email address is required for admin account"


def test_create_superuser_with_no_password(user_factory):
    """Test creating a superuser without a password raises an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=True, password=None)
    assert str(err.value) == "Superuser must have a password"


def test_user_email_incorrect(user_factory):
    """Test that an Error is raised when a non valid email is provided"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email="gmail.com")
    assert str(err.value) == "You must provide a valid email address"


def test_profile_str(profile):
    """Test the profile model string representation"""
    assert profile.__str__() == f"{profile.user.username}'s profile"


@pytest.fixture
def user_with_otp():
    # Create a user with OTP set
    user = User.objects.create(email="test@example.com", password="password")
    user_manager = User.objects
    user_manager.set_otp(user, 123456)
    return user


@pytest.mark.django_db
def test_verify_otp_successful(user_with_otp):
    # Verify OTP for the user (should return True)
    user = user_with_otp
    user_manager = User.objects
    result = user_manager.verify_otp(user, 123456)

    # Assert that OTP is verified, user is active, and OTP is cleared
    assert result is True
    assert user.is_active
    assert user.otp is None
    assert user.otp_expiration is None


@pytest.mark.django_db
def test_verify_otp_expired(user_with_otp):
    # Set OTP expiration to a past time
    user = user_with_otp
    user.otp_expiration = timezone.now() - timedelta(minutes=10)
    user.save()
    user_manager = User.objects

    # Verify OTP for the user (should return False due to expiration)
    result = user_manager.verify_otp(user, 123456)

    # Assert that OTP verification fails, user is not active, and OTP is not cleared
    assert result is False
    assert not user.is_active
    assert user.otp is not None
    assert user.otp_expiration is not None


@pytest.mark.django_db
def test_verify_otp_incorrect(user_with_otp):
    # Verify OTP with an incorrect value (should return False)
    user_manager = User.objects
    result = user_manager.verify_otp(user_with_otp, 789123)

    # Assert that OTP verification fails, user is not active, and OTP is not cleared
    assert result is False
    assert not user_with_otp.is_active
    assert user_with_otp.otp is not None
    assert user_with_otp.otp_expiration is not None


# @pytest.mark.django_db
# def test_set_otp():
#     user = User.objects.create(email="test@example.com", password="password")
#     user_manager = User.objects  # Access the manager

#     user_manager.set_otp(user, 123456)

#     assert user.otp == 123456
#     assert user.otp_expiration >= timezone.now() + timedelta(minutes=9)  # OTP should expire within 9-10 minutes
#     assert user.otp_expiration <= timezone.now() + timedelta(minutes=10)
