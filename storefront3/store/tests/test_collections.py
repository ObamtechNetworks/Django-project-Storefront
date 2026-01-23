# organize the tests by usecases
# from django.contrib.auth.models import User => moved to conftest.py
from store.models import Collection
from rest_framework import status
# from rest_framework.test import APIClient # This is a test client for DRF
import pytest
from model_bakery import baker

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

@pytest.mark.django_db
class TestRetrieveCollection:
    def test_if_collection_exists_returns_200(self, api_client, authenticate_user):
        # Arrange
        authenticate_user(is_staff=False) # Simulate an authenticated user (not necessarily admin)
        
        # First, create a collection to retrieve
        collection = baker.make(Collection) # Using model_bakery to create a collection instance
        # the model-bakery library helps to create model instances for testing purposes
        
        # Act
        response = api_client.get(f'/store/collections/{collection.id}/')  # Retrieve the collection by its ID
        
        # Assert
        assert response.status_code == status.HTTP_200_OK # Check that the response status code is 200 OK
        assert response.data == {
            'id': collection.id,
            'title': collection.title,
            'products_count': 0  # Assuming no products are associated with the collection
        }
        def test_if_collection_does_not_exist_returns_404(self, api_client):
            # Arrange
            # No collection is created
            
            # Act
            response = api_client.get('/store/collections/99999/')
            
            # Assert
            assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    class TestUpdateCollection:
        def test_if_user_is_anonymous_returns_401(self, api_client):
            # Arrange
            collection = baker.make(Collection)
            
            # Act
            response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'updated'})
            
            # Assert
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
            # Arrange
            authenticate_user(is_staff=False)
            collection = baker.make(Collection)
            
            # Act
            response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'updated'})
            
            # Assert
            assert response.status_code == status.HTTP_403_FORBIDDEN

        def test_if_data_is_invalid_returns_400(self, api_client, authenticate_user):
            # Arrange
            authenticate_user(is_staff=True)
            collection = baker.make(Collection)
            
            # Act
            response = api_client.put(f'/store/collections/{collection.id}/', {'title': ''})
            
            # Assert
            assert response.status_code == status.HTTP_400_BAD_REQUEST

        def test_if_data_is_valid_returns_200(self, api_client, authenticate_user):
            # Arrange
            authenticate_user(is_staff=True)
            collection = baker.make(Collection)
            
            # Act
            response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'updated title'})
            
            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert response.data['title'] == 'updated title'

    @pytest.mark.django_db
    class TestDeleteCollection:
        def test_if_user_is_anonymous_returns_401(self, api_client):
            # Arrange
            collection = baker.make(Collection)
            
            # Act
            response = api_client.delete(f'/store/collections/{collection.id}/')
            
            # Assert
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

        def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user):
            # Arrange
            authenticate_user(is_staff=False)
            collection = baker.make(Collection)
            
            # Act
            response = api_client.delete(f'/store/collections/{collection.id}/')
            
            # Assert
            assert response.status_code == status.HTTP_403_FORBIDDEN

        def test_if_collection_exists_returns_204(self, api_client, authenticate_user):
            # Arrange
            authenticate_user(is_staff=True)
            collection = baker.make(Collection)
            
            # Act
            response = api_client.delete(f'/store/collections/{collection.id}/')
            
            # Assert
            assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    class TestListCollections:
        def test_list_collections_returns_200(self, api_client):
            # Arrange
            baker.make(Collection, _quantity=3)
            
            # Act
            response = api_client.get('/store/collections/')
            
            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert len(response.data) == 3
