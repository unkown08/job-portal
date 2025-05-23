from rest_framework import serializers

from cloudinary.uploader import upload 

from ..custom_models.recruiter_models import Recruiter

from datetime import datetime

from account.serializers.job_seeker_serializer import UserEducationSerializer, UserJobExperienceSerializer, UserURLLinksSerializer
from  account.custom_models.job_seeker_models import JobSeeker

from job.models import JobResumes

class RegisterRecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ['id', 'company_name', 'company_bio', 'location']

    def validate(self, attrs):
        user = self.context['request'].user
        if Recruiter.objects.filter(recruiter=user).exists():
            raise serializers.ValidationError("Recruiter profile already exists for this user.")
        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        if user.role != 'recruiter':
            raise serializers.ValidationError("Only recruiters can create a recruiter profile.")
        return Recruiter.objects.create(recruiter=user, **validated_data)

class RecruiterLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter 
        fields = ["company_logo"]

    def update(self, instance, validated_data):
        image = validated_data.get('company_logo')
        if image:
            try:
                result = upload(image, folder="company_logos/")
                instance.company_logo = result["secure_url"]
            except Exception as e:
                raise serializers.ValidationError("An unexpected error occurred during image upload. Try again")
        instance.save()
        return instance

class UpdateRecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter 
        fields = ["company_name", "company_bio", "location", "company_website", "company_email", "company_size", "founded_year", "company_mobile_no"]

    def validate_founded_year(self, value):
        if value > datetime.today().date():
            raise serializers.ValidationError("Founded date cannot be in the future.")
        return value
    
class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter 
        fields = "__all__"

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    experiences = UserJobExperienceSerializer(many=True, read_only=True)
    educations = UserEducationSerializer(many=True, read_only=True)
    links = UserURLLinksSerializer(many=True, read_only=True)

    class Meta:
        model = JobSeeker
        fields = "__all__"

class JobSeekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = ['id'] 

class JobResumeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='applicant.user.username', read_only=True)
    applicant = JobSeekerSerializer(read_only=True)
    class Meta:
        model = JobResumes
        fields = ["id", "applicant", "username", "resume", "status", "uploaded_at"]

