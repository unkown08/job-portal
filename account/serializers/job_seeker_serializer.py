import logging

from rest_framework import serializers

from ..custom_models.job_seeker_models import JobSeeker, Education, Experience, UserLink

from job.models import JobResumes

from ..utils.validators import date_validation

from cloudinary.uploader import upload 

logger = logging.getLogger(__name__)

class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = "__all__"

class UploadProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
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
        user = self.context['request'].user 
        job_seeker = user.job_seeker_profile 
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
        user = self.context['request'].user
        job_seeker = user.job_seeker_profile 
        return Experience.objects.create(job_seeker=job_seeker, **validated_data)
    
class UserURLLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLink
        fields = ['id', 'name', 'url']

    def create(self, validated_data):
        user = self.context['request'].user
        job_seeker = user.job_seeker_profile 
        return UserLink.objects.create(job_seeker=job_seeker, **validated_data)

class UserResumesSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResumes
        fields = ["id", "resume", "status"]