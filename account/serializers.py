import logging

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from .models import CustomUser

from .utils.validators import password_validation
from .utils.formatters import white_space_formatter

from cloudinary.uploader import upload 

logger = logging.getLogger(__name__)

class RegisterUserSerailizer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id','username', 'email', 'password', 'profile_picture']

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
        result = {"secure_url": "https://res.cloudinary.com/dz87hmkzn/image/upload/v1716191715/oiudcncjhzzttodpymtq.webp"}
        validated_data['profile_picture'] = result['secure_url']

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

class UploadPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

    def update(self, instance, validated_data):
        image = validated_data.get('profile_picture')
        if image:
            try:
                result = upload(image, folder="profile_pictures/")
            except Exception as e:
                logger.error(f"Unexpected error during image upload: {e}")
                raise serializers.ValidationError("An unexpected error occurred during image upload. Try again")
        else:
            raise serializers.ValidationError("Need to attach a valid image")            
        
        instance.profile_picture = result["secure_url"]
        instance.save()
        return instance

