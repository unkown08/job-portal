from rest_framework import serializers

from .models import Jobs

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

