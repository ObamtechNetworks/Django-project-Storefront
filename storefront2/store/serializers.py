"""Serializer for Product model
What's a Serializer?
A serializer in Django REST Framework is responsible for converting complex data types, such as Django models/objects,
into native Python datatypes that can then be easily rendered into JSON, XML, or other content types.
"""
from decimal import Decimal
from rest_framework import serializers

from store.models import Product, Collection, Review

# through this we can include nested serializer object in the product serializer
# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

# class ProductSerializer(serializers.Serializer):
    # Define the fields that you want to serialize
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price') # source is used to map model field name to serializer field name, here we are renaming unit_price to price
    
    # creating custom serialized field that is not present in the model
    # this field will be read-only, we cannot use it to update or create a product
    # price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
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
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail' # this should be the name of the url pattern for the
    # ) # we would need to pass the request context in the Product 'view' while initializing the serializer for this to work
    
    
    # # this method is used by the SerializerMethodField to get the value for the field
    # # we converted the float to Decimal for consistency with unit_price field type
    # def calculate_tax(self,product: Product):
    #     return product.unit_price * Decimal(1.1)
    
# LET'S LEARN ABOUT MODEL SERIALIZER WHICH IS A MORE CONCISE WAY TO CREATE SERIALIZERS FOR DJANGO MODELS
# A ModelSerializer is a type of serializer that is tied to a specific Django model.
class ProductSerializer(serializers.ModelSerializer):
    # we can override the model field attributes here if needed
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source='unit_price'
    # )  # renaming unit_price to price
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )  # using hyperlinked related field for collection, by default model serializer would use PrimaryKeyRelatedField

    class Meta:
        model = Product  # specify the model to be serialized
        fields = [
            'id',
            'title',
            'description',
            'slug',
            'inventory',
            'unit_price',
            'price_with_tax',
            'collection',
        ]  # specify the fields to be included in the serialization
        # note the order matters here, it will be the order in the serialized output
        # we can do __all__ to include all fields, but it's not recommended for production code
        # alternatively we can use exclude = ['description'] to exclude specific fields

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    # let's override the create and update methods to customize the behavior when creating or updating a product
    # but we don't need to override these unless we want to customize the behavior
    # def create(self, validated_data):
    #     product = Product(**validated_data) # unpack the validated data dictionary to create a Product instance
    #     product.other = 1
    #     product.save() # save the instance to the database
    #     return product
    
    # overriding the update method
    # but we don't need to override this unless we want to customize the update behavior
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.slug = validated_data.get('slug', instance.slug)
    #     instance.unit_price = validated_data.get('unit_price', instance.unit_price)
    #     instance.inventory = validated_data.get('inventory', instance.inventory)
    #     instance.collection = validated_data.get('collection', instance.collection)
    #     instance.save() # save the updated instance to the database
    #     return instance
    
    # we can also add custom validation to the serializer fields
    # a sample field-level validation method
    # def validate(self, data):
    #     # object-level validation
    #     if data['password'] != data['confirm_password']:
    #         raise serializers.ValidationError("Passwords do not match")
    #     return data
    
# we can also create a serializer for the Collection model if needed
class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
        
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count'] # products_count will be annotated in the view

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']
        
    # let's override the create method for creating a review
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)