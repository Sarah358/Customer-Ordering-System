import pytest
from django.urls import reverse, reverse_lazy
from rest_framework import status
from rest_framework.test import APIClient

# Import your factories
from ..factories import ProfileFactory


@pytest.mark.django_db
def test_get_profile(base_user):
    # Create a profile using the ProfileFactory
    profile = ProfileFactory(user=base_user)

    # Create an instance of the APIClient
    api_client = APIClient()

    # Use the APIClient to simulate an authenticated request
    api_client.force_authenticate(user=base_user)

    # Make a GET request to the GetProfileAPIView
    url = reverse("profiles:get_profile")
    response = api_client.get(url)

    # Check that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK

    # Check that the response contains the expected data
    assert response.data["username"] == base_user.username
    assert response.data["phone_number"] == profile.phone_number


@pytest.mark.django_db
def test_update_profile(base_user):
    # Create an instance of the APIClient

    api_client = APIClient()

    # Use the APIClient to simulate an authenticated request
    api_client.force_authenticate(user=base_user)

    # Prepare data for updating the profile
    updated_data = {
        "phone_number": "+254799757242",
        "city": "Mombasa",
        "address": "2000",
    }

    # Make a PATCH request to the UpdateProfileAPIView using reverse_lazy
    url = reverse_lazy("profiles:update_profile", kwargs={"username": base_user.username})
    response = api_client.patch(url, data=updated_data, format="json")

    # Check that the response status code is 200 OK
    assert response.status_code == status.HTTP_200_OK
