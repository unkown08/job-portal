from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# Create your views here.

from .serializers import RegisterUserSerailizer
from rest_framework_simplejwt.tokens import RefreshToken

class Test(APIView):
    def get(self, request):
        return Response({"message": "Working"}, status=status.HTTP_200_OK)
    
class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterUserSerailizer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            user_data = RegisterUserSerailizer(user).data
            response = Response({"message": "user created successfully", "user": user_data}, status=status.HTTP_200_OK)
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
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)