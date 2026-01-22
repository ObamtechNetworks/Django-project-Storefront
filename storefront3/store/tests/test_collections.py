# organize the tests by usecases
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient # This is a test client for DRF
import pytest

@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip(reason="demonstration of test structure") # This decorator can be used to skip a test
    def test_if_user_is_anonymous_returns_401(self):
        # Every test should have three parts - the triple AAA
        
        # Arrange => where we set up the conditions for the test
        # In this case, no setup is needed for an anonymous user
        
        # Act -> where we kickoff the behavior we want to test
        client = APIClient() # Create an instance of the test client
        response = client.post('/store/collections/', {'title': 'a'}) # Make a POST request to create a collection
        
        # Assert -> where we verify the behavior we expected
        assert response.status_code == status.HTTP_401_UNAUTHORIZED # Check that the response status code is 401 Unauthorized
        
    def test_if_user_is_not_admin_returns_403(self):
        # Arrange
        # Act
        client = APIClient()
        client.force_authenticate(user={}) # Simulate an authenticated user who is not an admin
        response = client.post('/store/collections/', {'title': 'a'})
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN # Check that the response status code is 403 Forbidden
    
    def test_if_data_is_invalid_returns_400(self):
        # Arrange
        # Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True)) # Simulate an authenticated admin user
        response = client.post('/store/collections/', {'title': ''}) # Send invalid data (empty title)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST # Check that the response status code is 400 Bad Request
        # Optionally, we can also check the error message in the response
        assert response.data['title'] is not None
        
    def test_if_data_is_valid_returns_201(self):
        # Arrange
        # Act
        client = APIClient()
        client.force_authenticate(user=User(is_staff=True)) # Simulate an authenticated admin user
        response = client.post('/store/collections/', {'title': 'a'}) # Send valid data
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED # Check that the response status code is 201 Created
        assert response.data['id'] > 0 # Check that the response contains a valid collection ID