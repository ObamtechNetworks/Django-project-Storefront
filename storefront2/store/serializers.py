"""Serializer for Product model
What's a Serializer?
A serializer in Django REST Framework is responsible for converting complex data types, such as Django models/objects,
into native Python datatypes that can then be easily rendered into JSON, XML, or other content types.
"""
from decimal import Decimal
from rest_framework import serializers

from store.models import Product, Collection

# through this we can include nested serializer object in the product serializer
class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)

class ProductSerializer(serializers.Serializer):
    # Define the fields that you want to serialize
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') # source is used to map model field name to serializer field name, here we are renaming unit_price to price
    
    # creating custom serialized field that is not present in the model
    # this field will be read-only, we cannot use it to update or create a product
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    # Serializing related objects ---------------------------------- using primary key related field
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )  # this will serialize the related collection as its primary key (id)
    
    # -------------------------------------------------- using StringRelatedField
    # we can also use StringRelatedField to serialize the related object using its __str__ method
    # collection = serializers.StringRelatedField() # this will serialize the related collection using its __str__ method
    # however the above takes more time as it needs to fetch the related object from the database
    # a way to optimize this is to use select_related in the 'view' when fetching the products like this: Product.objects.select_related('collection').all()
    
    # -------------------------------------------------- using nested serializer, i.e another serializer class
    # we can also use nested serializer to serialize the related object
    # collection = CollectionSerializer() # this will serialize the related collection using the CollectionSerializer
    
    # -------------------------------------------------- using HyperlinkedRelatedField, dependencies: context in view and url pattern name
    # another way to serilize related object is to use hyperlinked related field
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail' # this should be the name of the url pattern for the
    ) # we would need to pass the request context in the Product 'view' while initializing the serializer for this to work
    
    
    # this method is used by the SerializerMethodField to get the value for the field
    # we converted the float to Decimal for consistency with unit_price field type
    def calculate_tax(self,product: Product):
        return product.unit_price * Decimal(1.1)