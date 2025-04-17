from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterUserSerailizer, LoginUserSerailizer

class Test(APIView):
    def get(self, request):
        return Response({"message": "Working"}, status=status.HTTP_200_OK)
    
class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterUserSerailizer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        user_data = RegisterUserSerailizer(user).data
        response = Response({"message": "user created successfully", "data": user_data}, status=status.HTTP_200_OK)
        response.set_cookie(
            "access_token",
            str(refresh.access_token),
            samesite=None,
            secure=True,
            httponly=True
        )
        response.set_cookie(
            "refresh_token",
            str(refresh),
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

