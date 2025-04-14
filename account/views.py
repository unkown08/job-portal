from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
# Create your views here.


class Test(APIView):
    def get(self, request):
        return Response({"message": "Working"}, status=status.HTTP_200_OK)