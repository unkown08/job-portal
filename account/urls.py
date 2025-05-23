from django.urls import path 
from .views import job_seeker_views, user_view, recruiter_views

urlpatterns = [
    path("register/", user_view.RegisterUseView.as_view(), name="register_user"),
    path("delete/", user_view.DeleteUserView.as_view(), name="delete_user"), 
    path("login/", user_view.LoginUserView.as_view(), name="login_user"),
    path("logout/", user_view.LogoutView.as_view(), name='logout_user'),
    path("change-password/", user_view.ChangePasswordView.as_view(), name="change_password"),
    path("job_seeker/upload-profile-picture/", job_seeker_views.UploadPhotoView.as_view(), name="profile_picture"),
    path("job_seeker/update-info/", job_seeker_views.UpdateUserInfoView.as_view(), name="update_user_info"),
    path("job_seeker/education/", job_seeker_views.UserEducationView.as_view(), name='add_user_education'),
    path("job_seeker/education/<int:pk>/", job_seeker_views.UserEducationView.as_view(), name="update_user_education"),
    path("job_seeker/experience/", job_seeker_views.UserJobExperienceView.as_view(), name="add_user_experience"),
    path("job_seeker/experience/<int:pk>/", job_seeker_views.UserJobExperienceView.as_view(), name="update_user_experience"),
    path("job_seeker/url-link/", job_seeker_views.UserURLLinksView.as_view(), name="add_user_urls"),
    path("job_seeker/url-link/<int:pk>/", job_seeker_views.UserURLLinksView.as_view(), name="update_user_urls"),
    path("job_seeker/info/", job_seeker_views.GetJobSeekerInfoView.as_view(), name="job_seeker_info"),
    path("job_seeker/resumes/", job_seeker_views.GetAppliedJobsInfo.as_view(), name="applied_jobs_info"),

    path("recruiter/register/", recruiter_views.RecruiterRegisterView.as_view(), name="register_recruiter"),
    path("recruiter/upload-company-logo/", recruiter_views.RecruiterLogoView.as_view(), name="recruiter_company_logo"),
    path("recruiter/update-info/", recruiter_views.UpdateRecruiterProfileView.as_view(), name="update_recruiter_profile"),
    path("recruiter/info/<int:pk>/", recruiter_views.GetRecruiterInfoView.as_view(), name="recruiter-info"),
    path("recruiter/job_seeker/info/<int:pk>/", recruiter_views.GetUserProfileView.as_view(), name="job_seeker_profile"),
    path("recruiter/resumes/<int:pk>/", recruiter_views.ListResumesAndSetStatusView.as_view(), name="list_jobs"),
    path("recruiter/status/<int:pk>/", recruiter_views.ListResumesAndSetStatusView.as_view(), name="set_status"),
]

