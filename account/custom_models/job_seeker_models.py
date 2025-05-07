from django.db import models
from cloudinary.models import CloudinaryField

class JobSeeker(models.Model):
    user = models.OneToOneField('account.CustomUser', on_delete=models.CASCADE, related_name="job_seeker_profile")
    bio = models.TextField(max_length=256, blank=True)
    profile_picture = CloudinaryField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Education(models.Model):
    job_seeker  = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name="educations")
    institution_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Experience(models.Model):
    job_seeker = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name="experiences")
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserLink(models.Model):
    job_seeker = models.ForeignKey('account.CustomUser', on_delete=models.CASCADE, related_name="links")
    name = models.CharField(max_length=100)  
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)