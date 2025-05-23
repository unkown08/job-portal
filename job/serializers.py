from rest_framework import serializers

from .models import Jobs, JobResumes

class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs 
        fields = "__all__"
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        if not hasattr(user, 'recruiter_profile'):
            raise serializers.ValidationError("User does not have a recruiter profile.")

        recruiter = user.recruiter_profile

        return Jobs.objects.create(recruiter=recruiter, **validated_data)
    
class JobResumeApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResumes
        fields = ["id", "status", "resume"]

    def create(self, validated_data):
        user = self.context['request'].user.job_seeker_profile
        job = self.context['job']
        return JobResumes.objects.create(applicant=user, job=job, **validated_data)

