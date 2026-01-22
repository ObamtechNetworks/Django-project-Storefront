import pytest
from rest_framework.test import APIClient

from django.contrib.auth.models import User

@pytest.fixture
def api_client():
    return APIClient()  # Provide a DRF APIClient instance for tests

# global fixture to authenticate user
@pytest.fixture
def authenticate_user(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))
    return do_authenticate  # Using the fixture to create a collection