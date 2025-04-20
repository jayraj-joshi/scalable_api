from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserModel
from .serializers import UserModelSerializer

class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
