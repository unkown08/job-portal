from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..serializers.recruiter_serializer import RegisterRecruiterSerializer, RecruiterLogoSerializer, UpdateRecruiterProfileSerializer, RecruiterProfileSerializer, JobSeekerProfileSerializer, JobResumeSerializer

from django.shortcuts import get_object_or_404

from ..authentication import IsRecruiter
from ..custom_models.recruiter_models import Recruiter

from account.custom_models.job_seeker_models import JobSeeker

from job.models import Jobs, JobResumes

class RecruiterRegisterView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request):
        serializer = RegisterRecruiterSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecruiterLogoView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request):
        recruiter = get_object_or_404(Recruiter, recruiter=request.user)
        serializer = RecruiterLogoSerializer(recruiter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateRecruiterProfileView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request):
        recruiter = get_object_or_404(Recruiter, recruiter=request.user)
        serializer = UpdateRecruiterProfileSerializer(recruiter, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetRecruiterInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        recruiter = get_object_or_404(Recruiter, pk=pk)
        serializer = RecruiterProfileSerializer(recruiter)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetUserProfileView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def get(self, request, pk):
        job_seeker = get_object_or_404(JobSeeker, pk=pk)
        serializer = JobSeekerProfileSerializer(job_seeker)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
    