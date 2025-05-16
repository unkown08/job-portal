from django.urls import path 
from . import views

urlpatterns = [
    path("register/", views.RegisterJobView.as_view(), name="register_job"),
    path("delete/<int:pk>/", views.DeleteJobView.as_view(), name="delete_job"),
    path("get-jobs/", views.GetRecuiterJobsView.as_view(), name="get_jobs"),
    
    path("apply/<int:pk>/", views.ApplyForJobView.as_view(), name="apply_for_job"),
    path("get-resumes/<int:pk>/", views.ListResumesAndSetStatusView.as_view(), name="list_jobs"),
    path("set-status/<int:pk>/", views.ListResumesAndSetStatusView.as_view(), name="set_status"),

    path("get-job_seeker-profile/<int:pk>/", views.GetUserProfileView.as_view(), name="job_seeker_profile"),

    path("all-jobs/", views.ListJobsView.as_view(), name="all_jobs"),
    path("<int:pk>/", views.ListSelectedJobView.as_view(), name="selected_job"),
]
