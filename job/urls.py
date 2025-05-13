from django.urls import path 
from . import views

urlpatterns = [
    path("register/", views.RegisterJobView.as_view(), name="register_job"),
    path("get-jobs/", views.GetRecuiterJobsView.as_view(), name="get_jobs"),
    
    path("apply/<int:pk>/", views.ApplyForJobView.as_view(), name="apply_for_job"),
]
