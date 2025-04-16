import re
import logging
from rest_framework import serializers
from .models import CustomUser

logger = logging.getLogger(__name__)

class RegisterUserSerailizer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'password']

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_password(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Password must be at least 5 characters long" 
            )
        if not re.search(r'[^a-zA-Z0-9]', value):
            raise serializers.ValidationError(
                "Password must have at least one special character" 
            )
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Password must have at least one upper case character"
            )
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError(
                "Password must have at least one number character"
            )
        return value
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user 

