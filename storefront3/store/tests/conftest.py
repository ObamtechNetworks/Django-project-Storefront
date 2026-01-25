import pytest
from rest_framework.test import APIClient

from django.contrib.auth import get_user_model

@pytest.fixture
def api_client():
    return APIClient()  # Provide a DRF APIClient instance for tests

# global fixture to authenticate user
@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate(is_staff=False):
        User = get_user_model()  # This gets your custom User model (core.User)
        user = User.objects.create_user(
            username=f'testuser{User.objects.count()}@test.com',  # Use email if that's your username field
            password='testpass123',
            is_staff=is_staff
        )
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate