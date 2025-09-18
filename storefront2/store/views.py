from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
from django.http import HttpResponse
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Collection, Product
from .serializers import CollectionSerializer, ProductSerializer

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