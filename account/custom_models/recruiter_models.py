from django.db import models 
from cloudinary.models import CloudinaryField

class Recruiter(models.Model):
    SIZE_CHOICES = [
        ("1-10", "1-10 employees"),
        ("11-50", "11-50 employees"),
        ("51-100", "51-100 employees"),
        ("101-500", "101-500 employees"),
        ("501-1000", "501-1000 employees"),
        ("1000+", "1000+ employees"),
    ]
    recruiter = models.OneToOneField('account.CustomUser', on_delete=models.CASCADE, related_name="recruiter_profile")
    company_name = models.CharField(max_length=50)
    company_logo = CloudinaryField(blank=True)
    company_bio = models.TextField(max_length=256)
    location = models.CharField(max_length=50)
    company_website = models.URLField(blank=True)
    company_email = models.EmailField(blank=True)
    company_mobile_no = models.CharField(max_length=20, blank=True)
    company_size = models.CharField(max_length=30, choices=SIZE_CHOICES, blank=True)
    founded_year = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

