import logging

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from .models import CustomUser, Education, Experience, UserLink

from .utils.validators import password_validation, date_validation
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
                raise serializers.ValidationError("User is deactivated")
            
            refresh = RefreshToken.for_user(user)

            return {
                "username": user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        
        raise serializers.ValidationError("Must include both username and password.")

class ChangePasswordSerailizer(serializers.Serializer):
    username = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)
    current_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        return password_validation(value)
    
    def validate(self, data):
        current_password = data.get('current_password')
        username = data.get('username')
        if username and current_password:
            user = authenticate(username=username, password=current_password)
            if user is None:
                raise serializers.ValidationError("Invalid username or password")
            if not user.is_active:
                raise serializers.ValidationError("User us deactivated")
        return data
    
    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        return user 
    
class UpdateCustomUserFields(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'bio', 'location', 'first_name', 'last_name']

class UploadProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["profile_picture"]
    
    def update(self, instance, validated_data):
        image = validated_data.get('profile_picture')
        if image:
            try:
                result = upload(image, folder="profile_pictures/")
                instance.profile_picture = result["secure_url"]
            except Exception as e:
                logger.error(f"Unexpected error during image upload: {e}. Try again")
                raise serializers.ValidationError("An unexpected error occurred during image upload. Try again")
        instance.save()
        return instance

class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution_name', 'start_date', 'end_date']

    def validate(self, data):
        start_date = data.get("start_date", getattr(self.instance, 'start_date', None))
        end_date = data.get("end_date", getattr(self.instance, 'end_date', None))
        if end_date:
            date_validation(start_date, end_date)
        return data 
        
    def create(self, validated_data):
        job_seeker = self.context['request'].user
        return Education.objects.create(job_seeker=job_seeker, **validated_data)

class UserJobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['id', 'company_name', 'job_title', 'start_date', 'end_date', 'description']

    def validate(self, data):
        start_date = data.get("start_date", getattr(self.instance, 'start_date', None))
        end_date = data.get("end_date", getattr(self.instance, 'end_date', None))
        if end_date:
            date_validation(start_date, end_date)
        return data 

    def create(self, validated_data):
        job_seeker = self.context['request'].user
        return Experience.objects.create(job_seeker=job_seeker, **validated_data)
    
class UserURLLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLink
        fields = ['id', 'name', 'url']

    def create(self, validated_data):
        job_seeker = self.context['request'].user
        return UserLink.objects.create(job_seeker=job_seeker, **validated_data)