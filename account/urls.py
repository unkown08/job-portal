from django.urls import path 
from .views import job_seeker_views, user_view

urlpatterns = [
    path("user/register", user_view.RegisterUseView.as_view(), name="register_user"),
    path("user/delete/", user_view.DeleteUserView.as_view(), name="delete_user"), 
    path("user/login/", user_view.LoginUserView.as_view(), name="login_user"),
    path("user/logout/", user_view.LogoutView.as_view(), name='logout_user'),
    path("user/change-password/", user_view.ChangePasswordView.as_view(), name="change_password"),
    path("user/upload-picture/", job_seeker_views.UploadPhotoView.as_view(), name="profile_picture"),
    path("user/update-user-info/", job_seeker_views.UpdateUserInfoView.as_view(), name="update_user_info"),
    path("user/education/", job_seeker_views.UserEducationView.as_view(), name='add_user_education'),
    path("user/education/<int:pk>/", job_seeker_views.UserEducationView.as_view(), name="update_user_education"),
    path("user/experience/", job_seeker_views.UserJobExperienceView.as_view(), name="add_user_experience"),
    path("user/experience/<int:pk>/", job_seeker_views.UserJobExperienceView.as_view(), name="update_user_experience"),
    path("user/url-link/", job_seeker_views.UserURLLinksView.as_view(), name="add_user_urls"),
    path("user/url-link/<int:pk>/", job_seeker_views.UserURLLinksView.as_view(), name="update_user_urls"),
]
