from django.urls import path 
from . import views

urlpatterns = [
    path("test/", views.Test.as_view(), name="test"),
    path("registeruser/", views.RegisterUser.as_view(), name="register_user")
]
