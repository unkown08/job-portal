from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..serializers.user_serializers import RegisterUserSerailizer, LoginUserSerailizer, ChangePasswordSerailizer

class RegisterUseView(APIView):
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
        
class LoginUserView(APIView):
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
   
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerailizer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
   
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request):
        user = request.user
        user.delete()
        response = Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response 
    