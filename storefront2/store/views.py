from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
# these are django builtin HttpRequest and HttpResponse classes
# example view function
# def product_list(request):
#     return HttpResponse('ok')

# Now let's use Django REST framework to return JSON response
@api_view()
def product_list(request):
    queryset = Product.objects.all() # fetch all products from the database
    serializer = ProductSerializer(queryset, many=True) # serialize / convert queryset data to a list of dictionaries
    return Response(serializer.data) # return serialized data as JSON response

@api_view()
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
    product = get_object_or_404(Product, pk=id) # if not found, raises Http404 exception
    serializer = ProductSerializer(product) # serialize / convert object data to a dictionary
    return Response(serializer.data) # return serialized data as JSON response