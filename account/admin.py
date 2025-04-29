from django.contrib import admin
from .models import CustomUser, Education, UserLink, Experience
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(UserLink)