from django.db import models
from django.contrib.auth.models import AbstractUser
from .custom_models.recruiter_models import Recruiter
from .custom_models.job_seeker_models import JobSeeker

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('recruiter', 'Recruiter'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='job_seeker')
    def __str__(self):
        return self.username 
 