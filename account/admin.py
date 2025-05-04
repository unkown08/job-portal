from django.contrib import admin
from .models import CustomUser
from .custom_models.job_seeker_models import Education, UserLink, Experience, JobSeeker
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(UserLink)
admin.site.register(JobSeeker)