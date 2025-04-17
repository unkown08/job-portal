from django.urls import path 
from . import views

urlpatterns = [
    path("test/", views.Test.as_view(), name="test"),
    path("registeruser/", views.RegisterUser.as_view(), name="register_user"),
    path("login/", views.LoginUser.as_view(), name="login_user"),
    path("logout/", views.LogoutView.as_view(), name='logout_user'),
    path("upload-picture/", views.UploadPhotoView.as_view(), name="profile_picture")
]
