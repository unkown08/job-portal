from rest_framework import serializers

from .models import Jobs, JobResumes
from account.custom_models.job_seeker_models import JobSeeker

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs 
        fields = ["id", "job_type", "location", "job_experience", "job_title", "job_salary", "job_description", "number_of_openings"]
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        if not hasattr(user, 'recruiter_profile'):
            raise serializers.ValidationError("User does not have a recruiter profile.")

        recruiter = user.recruiter_profile

        return Jobs.objects.create(recruiter=recruiter, **validated_data)
    
class JobResumeApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResumes
        fields = ["id", "status"]

    def create(self, validated_data):
        user = self.context['request'].user.job_seeker_profile
        job = self.context['job']
        return JobResumes.objects.create(applicant=user, job=job, **validated_data)

class JobResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResumes
        fields = ["id", "resume", "status", "uploaded_at"]