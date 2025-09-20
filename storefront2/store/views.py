from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
from django.http import HttpResponse
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Collection, OrderItem, Product, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer, ReviewSerializer

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
    # queryset = Product.objects.all() # to allow filtering, we would override get_queryset method
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        # get all objects first
        queryset = Product.objects.all()
        # attempt to get the collection_id from query parameters
        collection_id = self.request.query_params.get('collection_id')
        # if collection_id is provided, filter the queryset
        if collection_id is not None:
            queryset = queryset.filter(collection_id=collection_id)
        
        # now return this queryset
        return queryset
    
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
    
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk']) # filter reviews by product_id from the URL
    
    serializer_class = ReviewSerializer
    
    # using a context object we can pass additional data to our serialzier
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
