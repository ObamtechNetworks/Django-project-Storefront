# from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
# from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework import status

from store.pagination import DefaultPagination

from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission # FullDjangoModelPermissions
from .models import Cart, CartItem, Collection, Customer, Order, OrderItem, Product, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CollectionSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, ReviewSerializer, ReviewSerializer, UpdateCartItemSerializer

# Create your views here.
# these are django builtin HttpRequest and HttpResponse classes
# example view function
# def product_list(request):
#     return HttpResponse('ok')

# Now let's use Django REST framework to return JSON response

"""
# NOTE: These types of views below are all called **funcition based views.**
@api_view(['GET', 'POST']) # specify allowed HTTP methods
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all() # fetch all products from the database
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data) # return serialized data as JSON response
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data) # deserialize / convert JSON data to a Product instance
        serializer.is_valid(raise_exception=True) # validate the data (this reduces code without needing if-else)
        # next is to save the data to the database
        serializer.save() # save the validated data to the database
        # return the created product data with 201 status code
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # print(serializer.validated_data) # we'd save in database in next lesson
        # return Response('ok')
    

@api_view(['GET', 'PATCH', 'PUT', 'DELETE']) # PUT is for full update, PATCH is for partial update
def product_detail(request, id):
    # fetch the product from the database
    # try: ===> replaced with get_object_or_404
    #     product = Product.objects.get(id=id)
    #     serializer = ProductSerializer(product) # serialize / convert object data to a dictionary
    #     return Response(serializer.data) # return serialized data as JSON response
    # # handle the case where product with given id does not exist
    # except Product.DoesNotExist:
    #     return Response({'error': 'Product not found'}, status.HTTP_404_NOT_FOUND)
    
    # ==> simplified using get_object_or_404
    # brought this outside the if-else since it's common to all methods
    product = get_object_or_404(Product, pk=id) # if not found, raises Http404 exception
    if request.method == 'GET':
        serializer = ProductSerializer(product) 
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data) # deserialize / convert JSON data to a Product instance
        serializer.is_valid(raise_exception=True) # validate the data (this reduces code without needing if-else)
        serializer.save() # save the validated data to the database
        return Response(serializer.data) # return the updated product data
    elif request.method == 'PATCH':
        serializer = ProductSerializer(product, data=request.data, partial=True) # partial=True allows partial updates
        serializer.is_valid(raise_exception=True) # validate the data (this reduces code without needing if-else)
        serializer.save() # save the validated data to the database
        return Response(serializer.data) # return the updated product data
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0: # check if the product is associated with any order items
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete() # delete the product from the database
        return Response(status=status.HTTP_204_NO_CONTENT) # return 204 No Content status code

@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def collection_detail(request, pk):
    collection = get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = CollectionSerializer(collection, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all() # annotate each collection with the count of its products
        serializer = CollectionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""
"""
# CLASS BASED VIEWS
class ProductList(APIView):
    # two methods, get method for GET requests, and post method for POST requests
    def get(self, request):
        queryset = Product.objects.select_related('collection').all() # fetch all products from the database
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data) # return serialized data as JSON response
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data) # deserialize / convert JSON data to a Product instance
        serializer.is_valid(raise_exception=True) # validate the data (this reduces code without needing if-else)
        # next is to save the data to the database
        serializer.save() # save the validated data to the database
        # return the created product data with 201 status code
        return Response(serializer.data, status=status.HTTP_201_CREATED)

"""
"""
class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id) # if not found, raises Http404 exception
        serializer = ProductSerializer(product) 
        return Response(serializer.data)
    
    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data) # deserialize / convert JSON data to a Product instance
        serializer.is_valid(raise_exception=True) # validate the data (this reduces code without needing if-else)
        serializer.save() # save the validated data to the database
        return Response(serializer.data) # return the updated product data
    
    def patch(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data, partial=True) # partial=True allows partial updates
        serializer.is_valid(raise_exception=True) # validate the data (this reduces code without needing if-else)
        serializer.save() # save the validated data to the database
        return Response(serializer.data) # return the updated product data
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0: # check if the product is associated with any order items
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete() # delete the product from the database
        return Response(status=status.HTTP_204_NO_CONTENT) # return 204 No Content status code


# Using Generic Class Based Views to reduce boilerplate code
class ProductList(ListCreateAPIView):
    
    # no logic let's make it consise:
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    
    # this method is needed to pass request context to serializer for HyperlinkedRelatedField
    def get_serializer_context(self):
        return {'request': self.request}
    
    # All these methods are useful if we want to customize the behaviour and add some logic
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # # override to pass request context to serializer for HyperlinkedRelatedField
    # def get_serializer_context(self):
    #     return {'request': self.request}
    

# customizing generic view
class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer
    # lookup_field = 'id' # this is used to specify the field to be used for lookup, default is 'pk'
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def delete(self, request, *args, **kwargs):
        product = self.get_object() # get the product instance
        if product.orderitems.count() > 0: # check if the product is associated with any order items
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().delete(request, *args, **kwargs) # call the superclass delete method to perform the deletion
    
# converting collection_list to class based generic view
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def delete(self, request, *args, **kwargs):
        collection = self.get_object()
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().delete(request, *args, **kwargs)
"""

# Learning about ViewSets
# advantage of viewsets is that we can combine multiple views into a single class
# and we can use routers to automatically generate the URL conf for the viewset
# this reduces boilerplate code and makes it easier to maintain
# we can use ModelViewSet which provides all the CRUD operations by default
# we can also use ReadOnlyModelViewSet which provides only read operations (GET)

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all() # brought this back since we are now using generic filtering
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly] # only admin users can edit products, others can only read
    # let's use generic filtering instead of manual filtering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # specify fields to filter by
    # filterset_fields = ['collection_id'] # allow filtering by collection_id
    filterset_class = ProductFilter # since we've created a custom filter class and defined fields to filter
    # pagination in django rest framework
    # pagination_class = PageNumberPagination
    pagination_class = DefaultPagination
    search_fields = ['title', 'description'] # allow searching by title and description
    ordering_fields = ['unit_price', 'last_update']
    # above line allows searching with ?search=keyword in the URL
    
    # Now we can remove the ovridden get_queryset method below
    # def get_queryset(self):
    #     # get all objects first
    #     queryset = Product.objects.all()
    #     # attempt to get the collection_id from query parameters
    #     collection_id = self.request.query_params.get('collection_id')
    #     # if collection_id is provided, filter the queryset
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
        
        # now return this queryset
        # return queryset
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        # product = self.get_object() # get the product instance
        # if product.orderitems.count() > 0: # check if the product is associated with any order items
        #     return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # writing above as:
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs) # call the superclass delete method to perform the deletion

# Viewset for Collections
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        # collection = self.get_object()
        # if collection.products.count() > 0:
        #     return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        # re-writing above as:
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
# we can also create a viewset for reviews if needed
class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all() # we won't use this since we want reviews for a specific product, cos .all() would return all reviews
    # to do a better implementation, we would override the get_queryset method
    
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk']) # filter reviews by product_id from the URL
    
    
    # using a context object we can pass additional data to our serialzier
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

# viewset for Cart model
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet,
                  DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product') # prefetch related items and products to reduce number of queries
    serializer_class = CartSerializer 
    

class CartItemViewSet(ModelViewSet,):
    # specify the http methods to allow
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    # serializer_class = CartItemSerializer
    
    # We want to dynamically return what serializer depending on the request method
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        # if it's patch or PUT we are using the updatecartitemserializer instead
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id=self.kwargs['cart_pk']) \
            .select_related('product')
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
# CREATE THE PROFILE API FOR CUSTOMERS
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser] # only admin users can view customer data
    # we can also use FullDjangoModelPermissions if we want to use django model permissions
    # permission_classes = [FullDjangoModelPermissions] or DjangoModelPermissions depending on whether we want to include 'view' permissions or not
    
    # def get_permissions(self):
    #     # PROTECT THE 'ME' ENDPOINT
    #     if self.action == 'me':
    #          return [IsAuthenticated()]
             
    #     # ALLOW PUBLIC ACCESS TO OTHER GET REQUESTS (e.g. Viewing product lists)
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
        
    #     return [IsAuthenticated()]
    
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk=None):
        return Response("Ok")
    
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        # We look up by user_id. 
        # If not found, we create one using 'defaults' to fill in the required unique email.
        customer, created = Customer.objects.get_or_create(
            user_id=request.user.id,
            defaults={'email': request.user.email} 
        )
        
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = CustomerSerializer(
                request.user.customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

# view for orders
class OrderViewSet(ModelViewSet):
    # serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    # overriding the create method in the ModelViewSet with logics to return created order
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context={'user_id': self.request.user.id})
        serializer.is_valid (raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    # dynamically return serializer class based on request method
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer
    
    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}
    
    # ensure order being displayed belongs to the user making the request
    def get_queryset(self):
        user = self.request.user
        
        # if the user is staff, return all orders
        if user.is_staff:
            return Order.objects.all()
        
        # will need to refactor this line below to ensure command query separation
        # the overriding of the get_queryset and the use of get or create is not ideal
        (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)