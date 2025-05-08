from rest_framework import serializers

from ..custom_models.recruiter_models import Recruiter

class RegisterRecruiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recruiter
        fields = ['company_name', 'company_bio', 'location']
    
    def create(self, validated_data):
        user = self.context['request'].user
        if user.role != 'recruiter':
            raise serializers.ValidationError("Only recruiters can create a recruiter profile.")
        return Recruiter.objects.create(recruiter=user, **validated_data)