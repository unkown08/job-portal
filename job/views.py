from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from account.authentication import IsRecruiter
from rest_framework.permissions import IsAuthenticated

from .serializers import JobsSerializer
from .models import Jobs

class RegisterJobView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request):
        serializer = JobsSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetJobsView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter] 
    def get(self, request):
        recruiter = request.user.recruiter_profile
        jobs = Jobs.objects.filter(recruiter=recruiter)
        serializer = JobsSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)