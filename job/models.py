from django.db import models
from account.custom_models.recruiter_models import Recruiter
from account.custom_models.job_seeker_models import JobSeeker
from django.core.validators import MinValueValidator
# Create your models here.

class Jobs(models.Model):
    EXPERIENCE_CHOICES = [
        ('0', 'No experience'),
        ('1-2', '1 to 2 year'),
        ('2-5', '2 to 5 years'),
        ('5-10', '5 to 10 years'),
        ('10', '10+ years'),
    ]
    JOB_TYPE_CHOICES = [('FT', 'Full-Time'), ('PT', 'Part-Time'), ('CT', 'Contract')]

    recruiter = models.OneToOneField(Recruiter, on_delete=models.CASCADE, related_name="job")
    job_description = models.TextField(max_length=500)
    job_salary = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    job_experience = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    number_of_openings = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

class JobResumes(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name="resumes")
    applicant = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to='pdfs/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    uploaded_at = models.DateTimeField(auto_now_add=True)
