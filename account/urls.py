from django.urls import path 
from . import views

urlpatterns = [
    path("user/register", views.RegisterUseView.as_view(), name="register_user"),
    path("user/delete/", views.DeleteUserView.as_view(), name="delete_user"), 
    path("user/login/", views.LoginUserView.as_view(), name="login_user"),
    path("user/logout/", views.LogoutView.as_view(), name='logout_user'),
    path("user/upload-picture/", views.UploadPhotoView.as_view(), name="profile_picture"),
    path("user/change-password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("user/update-user-info/", views.UpdateUserInfoView.as_view(), name="update_user_info"),
    path("user/education/", views.UserEducationView.as_view(), name='add_user_education'),
    path("user/education/<int:pk>/", views.UserEducationView.as_view(), name="update_user_education"),
    path("user/experience/", views.UserJobExperienceView.as_view(), name="add_user_experience"),
    path("user/experience/<int:pk>/", views.UserJobExperienceView.as_view(), name="update_user_experience"),
]
