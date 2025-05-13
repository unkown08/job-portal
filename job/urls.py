from django.urls import path 
from . import views

urlpatterns = [
    path("register/", views.RegisterJobView.as_view(), name="register_job"),
    path("get-jobs/", views.GetJobsView.as_view(), name="get_jobs"),
]
