from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegisterUserSerailizer, LoginUserSerailizer, UploadPhotoSerializer

class Test(APIView):
    def get(self, request):
        return Response({"message": "Working"}, status=status.HTTP_200_OK)
    
class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterUserSerailizer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.save()
        user_data = RegisterUserSerailizer(data['user']).data
        response = Response(
            {"message": "User created successfully", "data": user_data}, 
            status=status.HTTP_201_CREATED
        )
        response.set_cookie(
            "access_token",
            data['access'],
            samesite=None,
            secure=True,
            httponly=True
        )
        response.set_cookie(
            "refresh_token",
            data['refresh'],
            samesite=None,
            secure=True,
            httponly=True
        )
        return response
        
class LoginUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginUserSerailizer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data
        response = Response(data['username'], status=status.HTTP_200_OK)
        response.set_cookie(
            key='access_token',
            value=data['access'],
            httponly=True,
            secure=True,
            samesite=None
        )
        response.set_cookie(
            key='refresh_token',
            value=data['refresh'],
            httponly=True,
            secure=True,
            samesite=None
        )
        return response

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        response = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
    
class UploadPhotoView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UploadPhotoSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "uploaded successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)