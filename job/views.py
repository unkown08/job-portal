from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from account.authentication import IsRecruiter

from .serializers import JobsSerializer, JobResumeSerializer, JobResumeApplySerializer, JobSeekerProfileSerializer
from .models import Jobs, JobResumes

from account.custom_models.job_seeker_models import JobSeeker

class RegisterJobView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request):
        serializer = JobsSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteJobView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def delete(self, request, pk):
        job = get_object_or_404(Jobs, pk=pk)
        job.delete()
        return Response({"message": "deleted job"}, status=status.HTTP_204_NO_CONTENT)

class GetRecuiterJobsView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter] 
    def get(self, request):
        recruiter = request.user.recruiter_profile
        jobs = Jobs.objects.filter(recruiter=recruiter)
        serializer = JobsSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ApplyForJobView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        job = get_object_or_404(Jobs, pk=pk)
        serializer = JobResumeApplySerializer(data=request.data, context={"request": request, "job": job})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListResumesAndSetStatusView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def get(self, request, pk):
        job = get_object_or_404(Jobs, pk=pk)
        all_applications = JobResumes.objects.filter(job=job)
        serializer = JobResumeSerializer(all_applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, pk):
        resume = get_object_or_404(JobResumes, pk=pk)
        serializer = JobResumeSerializer(resume, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Changed Status"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request, pk):
        job_seeker = get_object_or_404(JobSeeker, pk=pk)
        serializer = JobSeekerProfileSerializer(job_seeker)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ListJobsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        all_jobs = Jobs.objects.all()
        serializer = JobsSerializer(all_jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)