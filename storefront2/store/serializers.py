"""Serializer for Product model
What's a Serializer?
A serializer in Django REST Framework is responsible for converting complex data types, such as Django models/objects,
into native Python datatypes that can then be easily rendered into JSON, XML, or other content types.
"""
from decimal import Decimal
from rest_framework import serializers

from store.models import Product

class ProductSerializer(serializers.Serializer):
    # Define the fields that you want to serialize
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') # source is used to map model field name to serializer field name
    
    # creating custom serialized field
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self,product: Product):
        return product.unit_price * Decimal(1.1)