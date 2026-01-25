from store.models import Collection, Customer, Order, OrderItem, Product
from rest_framework import status
import pytest
from model_bakery import baker

@pytest.fixture
def create_product(api_client):
    def do_create_product(product):
        return api_client.post('/store/products/', product)
    return do_create_product

@pytest.mark.django_db
class TestCreateProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product):
        # Arrange
        # create a collection to associate with the product
        collection = baker.make(Collection)
        product_data = {
            'title': 'New Product',
            'description': 'A description of the new product',
            'unit_price': 10.99,
            'collection': collection.id
        }
        
        # Act
        response = create_product(product_data)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user, create_product):
        # Arrange
        authenticate_user(is_staff=False)
        # create a collection to associate with the product
        collection = baker.make(Collection)
        product_data = {
            'title': 'New Product',
            'description': 'A description of the new product',
            'unit_price': 10.99,
            'collection': collection.id
        }
        
        # Act
        response = create_product(product_data)
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_invalid_returns_400(self, api_client, authenticate_user, create_product):
        # Arrange
        authenticate_user(is_staff=True)
        # create a collection to associate with the product
        collection = baker.make(Collection)
        product_data = {
            'title': '',  # Invalid title
            'description': 'A description of the new product',
            'unit_price': -5.00,  # Invalid price
            'collection': collection.id
        }
        
        # Act
        response = create_product(product_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_if_data_is_valid_returns_201(self, api_client, authenticate_user, create_product):
        # Arrange
        authenticate_user(is_staff=True)
        
        # create a collection to associate with the product
        collection = baker.make(Collection)
        product_data = {
            'title': 'New Product',
            'description': 'A description of the new product',
            'unit_price': 10.99,
            'slug': 'new-product',
            'inventory': 100,
            'collection': collection.id,
            'images': []
        }
        
        
        # Act
        response = create_product(product_data)
        
        
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == product_data['title']
        assert str(response.data['unit_price']) == str(product_data['unit_price'])

@pytest.mark.django_db
class TestListProducts:
    def test_list_products(self, api_client):
        # Arrange
        products_list = baker.make(Product, _quantity=5)
        
        # Act
        response = api_client.get('/store/products/')
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5
        
    def test_list_products_with_pagination(self, api_client):
        # Arrange
        products_list = baker.make(Product, _quantity=25)
        
        # Act
        response = api_client.get('/store/products/?page=2&page_size=10')
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 10
        assert response.data['count'] == 25
        
    def test_list_products_with_search(self, api_client):
        # Arrange
        baker.make(Product, title='Red Shirt')
        baker.make(Product, title='Blue Jeans')
        baker.make(Product, title='Green Hat')
        
        # Act
        response = api_client.get('/store/products/?search=Shirt')
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == 'Red Shirt'
    
    def test_list_products_with_ordering(self, api_client):
        # Arrange
        baker.make(Product, title='Product A', unit_price=20.00)
        baker.make(Product, title='Product B', unit_price=10.00)
        baker.make(Product, title='Product C', unit_price=30.00)
        
        # Act
        response = api_client.get('/store/products/?ordering=unit_price') # the actual test focuses here
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        prices = [product['unit_price'] for product in response.data['results']]
        assert prices == sorted(prices)
    
    def test_list_products_with_filtering(self, api_client):
        # Arrange
        collection1 = baker.make(Collection)
        collection2 = baker.make(Collection)
        baker.make(Product, title='Product A', collection=collection1)
        baker.make(Product, title='Product B', collection=collection2)
        baker.make(Product, title='Product C', collection=collection1)
        
        # Act
        response = api_client.get(f'/store/products/?collection_id={collection1.id}')
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        for product in response.data['results']:
            assert product['collection'] == collection1.id

@pytest.mark.django_db
class TestRetrieveProduct:
    def test_retrieve_product(self, api_client):
        # Arrange
        product = baker.make(Product)
        
        # Act
        response = api_client.get(f'/store/products/{product.id}/')
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id
        assert response.data['title'] == product.title
        assert str(response.data['unit_price']) == str(product.unit_price)
    
    def test_retrieve_nonexistent_product_returns_404(self, api_client):
        # Act
        response = api_client.get('/store/products/9999/')
        
        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_retrieve_product_includes_images(self, api_client):
        # Arrange
        product = baker.make(Product)
        baker.make('store.ProductImage', product=product, _quantity=3)
        
        # Act
        response = api_client.get(f'/store/products/{product.id}/')
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['images']) == 3
    
@pytest.mark.django_db
class TestDeleteProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product):
        # Arrange
        product = baker.make(Product)
        
        # Act
        response = api_client.delete(f'/store/products/{product.id}/')
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user, create_product):
        # Arrange
        authenticate_user(is_staff=False)
        product = baker.make(Product)
        
        # Act
        response = api_client.delete(f'/store/products/{product.id}/')
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_product_exists_returns_204(self, api_client, authenticate_user, create_product):
        # Arrange
        authenticate_user(is_staff=True)
        product = baker.make(Product)
        
        # Act
        response = api_client.delete(f'/store/products/{product.id}/')
        
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
    
    def test_if_product_associated_with_order_item_returns_405(self, api_client, authenticate_user, create_product):
        # Arrange
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        user = baker.make(User, is_staff=True)
        
        # Create customer - check if one already exists for this user
        customer, created = Customer.objects.get_or_create(user=user)
        
        product = baker.make(Product)
        order = baker.make(Order, customer=customer)
        baker.make(OrderItem, order=order, product=product)
        
        # Authenticate the user
        api_client.force_authenticate(user=user)

        # Act
        response = api_client.delete(f'/store/products/{product.id}/')
        
        # Assert
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.data['error'] == 'Product cannot be deleted because it is associated with an order item.'
        
@pytest.mark.django_db
class TestUpdateProduct:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_product):
        # Arrange
        product = baker.make(Product)
        update_data = {
            'title': 'Updated Title'
        }
        
        # Act
        response = api_client.put(f'/store/products/{product.id}/', update_data)
        
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(self, api_client, authenticate_user, create_product):
        # Arrange
        authenticate_user(is_staff=False)
        product = baker.make(Product)
        update_data = {
            'title': 'Updated Title'
        }
        
        # Act
        response = api_client.put(f'/store/products/{product.id}/', update_data)
        
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_data_is_valid_returns_200(self, api_client, authenticate_user, create_product):
        # Arrange
        authenticate_user(is_staff=True)
        product = baker.make(Product)
        update_data = {
            'title': 'Updated Title',
            'description': str(product.description),
            'unit_price': str(product.unit_price),
            'inventory': product.inventory,
            'slug': product.slug,
            'collection': product.collection.id
        }
        
        # Act
        response = api_client.put(f'/store/products/{product.id}/', update_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'
    
    def test_if_data_is_invalid_returns_400(self, api_client, authenticate_user, create_product):
        # Arrange
        authenticate_user(is_staff=True)
        product = baker.make(Product)
        update_data = {
            'title': '',  # Invalid title
            'description': str(product.description),
            'unit_price': '-10.00',  # Invalid price
            'inventory': product.inventory,
            'slug': product.slug,
            'collection': product.collection.id
        }
        
        # Act
        response = api_client.put(f'/store/products/{product.id}/', update_data)
        
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_partial_update_returns_200(self, api_client, authenticate_user, create_product):
        # Arrange
        authenticate_user(is_staff=True)
        product = baker.make(Product)
        update_data = {
            'title': 'Partially Updated Title'
        }
        
        # Act
        response = api_client.patch(f'/store/products/{product.id}/', update_data)
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Partially Updated Title'
