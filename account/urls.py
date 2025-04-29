from django.urls import path 
from .views import job_seeker_views

urlpatterns = [
    path("user/register", job_seeker_views.RegisterUseView.as_view(), name="register_user"),
    path("user/delete/", job_seeker_views.DeleteUserView.as_view(), name="delete_user"), 
    path("user/login/", job_seeker_views.LoginUserView.as_view(), name="login_user"),
    path("user/logout/", job_seeker_views.LogoutView.as_view(), name='logout_user'),
    path("user/upload-picture/", job_seeker_views.UploadPhotoView.as_view(), name="profile_picture"),
    path("user/change-password/", job_seeker_views.ChangePasswordView.as_view(), name="change_password"),
    path("user/update-user-info/", job_seeker_views.UpdateUserInfoView.as_view(), name="update_user_info"),
    path("user/education/", job_seeker_views.UserEducationView.as_view(), name='add_user_education'),
    path("user/education/<int:pk>/", job_seeker_views.UserEducationView.as_view(), name="update_user_education"),
    path("user/experience/", job_seeker_views.UserJobExperienceView.as_view(), name="add_user_experience"),
    path("user/experience/<int:pk>/", job_seeker_views.UserJobExperienceView.as_view(), name="update_user_experience"),
    path("user/url-link/", job_seeker_views.UserURLLinksView.as_view(), name="add_user_urls"),
    path("user/url-link/<int:pk>/", job_seeker_views.UserURLLinksView.as_view(), name="update_user_urls"),
]
