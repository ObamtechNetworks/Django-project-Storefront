from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    """Custom serializer for user creation that includes the 'name' field."""
    # birth_date = serializers.DateField(required=False)
    
    
    # extend the Meta class to inherit from the base serializer and change some fields
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'first_name', 'last_name', 'password', 'email'] #'birth_date']