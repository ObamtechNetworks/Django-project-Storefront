# organize the tests by usecases
# from django.contrib.auth.models import User => moved to conftest.py
from rest_framework import status
# from rest_framework.test import APIClient # This is a test client for DRF
import pytest

# test fixture to create a collection
@pytest.fixture
def create_collection(api_client):
    # A function that uses the api_client fixture to create a collection
    def do_create_collection(collection):
        # Use the api_client to send a POST request to create a collection
        return api_client.post('/store/collections/', collection)
    # Return the function to the test
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollection:
    # @pytest.mark.skip(reason="demonstration of test structure") # This decorator can be used to skip a test
    def test_if_user_is_anonymous_returns_401(self, create_collection):
        # Every test should have three parts - the triple AAA
        
        # Arrange => where we set up the conditions for the test
        # In this case, no setup is needed for an anonymous user
        
        # # Act -> where we kickoff the behavior we want to test
        # client = APIClient() # Create an instance of the test client ==> # removing this line to use the fixture instead
        
        response = create_collection({'title': 'a'})  # Using the fixture to create a collection

        # Assert -> where we verify the behavior we expected
        assert response.status_code == status.HTTP_401_UNAUTHORIZED # Check that the response status code is 401 Unauthorized
        
    def test_if_user_is_not_admin_returns_403(self, api_client, create_collection, authenticate_user):
        # Arrange
        authenticate_user(is_staff=False) # Simulate an authenticated user who is not an admin
        
        # Act
        # client = APIClient() => removing this line to use the fixture instead
        response = create_collection({'title': 'a'})  # Using the fixture to create a collection
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN # Check that the response status code is 403 Forbidden

    def test_if_data_is_invalid_returns_400(self, api_client, create_collection, authenticate_user):
        # Arrange
        authenticate_user(is_staff=True) # Simulate an authenticated admin user
        
        # Act
        response = create_collection({'title': ''}) # Using the fixture to send invalid data (empty title)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST # Check that the response status code is 400 Bad Request
        # Optionally, we can also check the error message in the response
        assert response.data['title'] is not None

    def test_if_data_is_valid_returns_201(self, api_client, create_collection, authenticate_user):
        # Arrange
        authenticate_user(is_staff=True) # Simulate an authenticated admin user
        
        # Act
        response = create_collection({'title': 'a'}) # Send valid data
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED # Check that the response status code is 201 Created
        assert response.data['id'] > 0 # Check that the response contains a valid collection ID