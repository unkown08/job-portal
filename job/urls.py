from django.urls import path 
from . import views

urlpatterns = [
    path("register/", views.RegisterJobView.as_view(), name="register_job"),
    path("delete/<int:pk>/", views.DeleteJobView.as_view(), name="delete_job"),
    path("get-jobs/", views.GetRecuiterJobsView.as_view(), name="get_jobs"),
    path("apply/<int:pk>/", views.ApplyForJobView.as_view(), name="apply_for_job"),
    path("all-jobs/", views.ListJobsView.as_view(), name="all_jobs"),
    path("<int:pk>/", views.ListSelectedJobView.as_view(), name="selected_job"),
]
