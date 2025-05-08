from rest_framework import serializers

from ..custom_models.recruiter_models import Recruiter

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