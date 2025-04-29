from django.urls import path 
from . import views

urlpatterns = [
    path("registeruser/", views.RegisterUseView.as_view(), name="register_user"),
    path("login/", views.LoginUserView.as_view(), name="login_user"),
    path("logout/", views.LogoutView.as_view(), name='logout_user'),
    path("upload-picture/", views.UploadPhotoView.as_view(), name="profile_picture"),
    path("password/update", views.ChangePasswordView.as_view(), name="change_password"),
    path("userinfo/update/", views.UpdateUserInfoView.as_view(), name="update_user_info"),
    path("education/add", views.UserEducationView.as_view(), name='add_user_education'),
    path("education/<int:pk>/update/", views.UserEducationView.as_view(), name="update_user_education"),
    path("deleteuser/", views.DeleteUserView.as_view(), name="delete_user")
]
