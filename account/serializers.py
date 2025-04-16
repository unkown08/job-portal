import logging
from rest_framework import serializers
from .models import CustomUser
from .utils.validators import password_validation
from .utils.formatters import white_space_formatter

logger = logging.getLogger(__name__)

class RegisterUserSerailizer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'password']

    def validate_username(self, value):
        value = white_space_formatter(value)
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_password(self, value):
        return password_validation(value)
    
    def create(self, validated_data):
        username = validated_data.get('username')
        formatted_username = white_space_formatter(username)
        validated_data['username'] = formatted_username
        user = CustomUser.objects.create_user(**validated_data)
        return user 

