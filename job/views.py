from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from account.authentication import IsRecruiter

from .serializers import JobsSerializer, JobResumeSerializer, JobResumeApplySerializer
from .models import Jobs, JobResumes

class RegisterJobView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request):
        serializer = JobsSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    