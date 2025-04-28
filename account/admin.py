from django.contrib import admin
from .models import CustomUser, Education
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Education)