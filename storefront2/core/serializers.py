from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from store.models import Customer

class UserCreateSerializer(BaseUserCreateSerializer):
    """Custom serializer for user creation that includes the 'name' field."""
    
    # extend the Meta class to inherit from the base serializer and change some fields
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email'] #'birth_date']
        
# Custom serializer for current user representation
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'email']