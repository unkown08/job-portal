import logging

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

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

        refresh = RefreshToken.for_user(user)

        return {
                "user": user,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
        }

class LoginUserSerailizer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if user is None:
                raise serializers.ValidationError("Invalid username or password")
            if not user.is_active:
                raise serializers.ValidationError("User us deactivated")
            
            refresh = RefreshToken.for_user(user)

            return {
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        
        raise serializers.ValidationError("Must include both username and password.")

