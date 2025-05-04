from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..serializers.job_seeker_serializer import UpdateCustomUserFields, UploadProfilePictureSerializer, UserEducationSerializer, UserJobExperienceSerializer, UserURLLinksSerializer

from django.shortcuts import get_object_or_404

from ..models import Education, Experience, UserLink, JobSeeker

class UploadPhotoView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        job_seeker, _ = JobSeeker.objects.get_or_create(user=request.user)
        serializer = UploadProfilePictureSerializer(job_seeker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "uploaded successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateUserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        updatable_fields = ['bio', 'location', 'first_name', 'last_name']

        data = {key: request.data[key] for key in updatable_fields if key in request.data}

        if not data:
            return Response({"error": "No valid fields provided to update."}, status=status.HTTP_400_BAD_REQUEST)
        job_seeker, _ = JobSeeker.objects.get_or_create(user=request.user)
        serializer = UpdateCustomUserFields(job_seeker, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User information updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserEducationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            education = get_object_or_404(Education, pk=pk, job_seeker=request.user)
            serializer = UserEducationSerializer(education)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            education = Education.objects.filter(job_seeker=request.user)
            serializer = UserEducationSerializer(education, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserEducationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        education = get_object_or_404(Education, pk=pk, job_seeker=request.user)
        serializer = UserEducationSerializer(education, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        education = get_object_or_404(Education, pk=pk, job_seeker=request.user)
        education.delete()
        return Response({"message": "Education deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class UserJobExperienceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            experience = get_object_or_404(Experience, pk=pk, job_seeker=request.user)
            serializer = UserJobExperienceSerializer(experience)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            experience = Experience.objects.filter(job_seeker=request.user)
            serializer = UserJobExperienceSerializer(experience, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = UserJobExperienceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk, job_seeker=request.user)
        serializer = UserJobExperienceSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        experience = get_object_or_404(Experience, pk=pk, job_seeker=request.user)
        experience.delete()
        return Response({"message": "Experience deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class UserURLLinksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            userlink = get_object_or_404(UserLink, pk=pk, job_seeker=request.user)
            serializer = UserURLLinksSerializer(userlink)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            userlinks = UserLink.objects.filter(job_seeker=request.user)
            serializer = UserURLLinksSerializer(userlinks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserURLLinksSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        userlink = get_object_or_404(UserLink, pk=pk, job_seeker=request.user)
        serializer = UserURLLinksSerializer(userlink, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        userlink = get_object_or_404(UserLink, pk=pk, job_seeker=request.user)
        userlink.delete()
        return Response({"message": "Experience deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

