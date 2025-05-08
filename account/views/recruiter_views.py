from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..serializers.recruiter_serializer import RegisterRecruiterSerializer

from ..authentication import IsRecruiter
from ..custom_models.recruiter_models import Recruiter

class RecruiterRegisterView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request):
        serializer = RegisterRecruiterSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# {"username": "wertsd", "password": "asdfAS@132", "role": "recruiter"}