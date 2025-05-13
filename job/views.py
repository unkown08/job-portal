from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from account.authentication import IsRecruiter
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterJobSerializer

class RegisterJobView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]
    def post(self, request):
        serializer = RegisterJobSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
