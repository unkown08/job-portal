from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from account.authentication import IsRecruiter

from .serializers import JobsSerializer, JobResumeApplySerializer
from .models import Jobs

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
    
class ListJobsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        job_type = request.query_params.get('job_type')
        job_experience = request.query_params.get('job_experience')
        location = request.query_params.get('location')
        search = request.query_params.get('search')

        queryset = Jobs.objects.all()

        if job_type:
            queryset = queryset.filter(job_type=job_type)

        if job_experience:
            queryset = queryset.filter(job_experience=job_experience)

        if location:
            queryset = queryset.filter(location=location)

        if search:
            queryset = queryset.filter(job_title__icontains=search)

        serializer = JobsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ListSelectedJobView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        job = get_object_or_404(Jobs, pk=pk)
        serializer = JobsSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
