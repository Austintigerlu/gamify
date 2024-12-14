from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializer import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def get_user(request):
    return Response({"message": "API is working!"})

# /api
@api_view(['GET'])
def api_root(request):
    return Response({
        "status": "success",
        "message": "Welcome to the Gamify API",
        "version": "1.0.0"
    })

@api_view(['GET'])
def get_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

#[POST] Create token on login 
#Url: /Token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

#[POST] Register User 
#Url: /register
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message': 'User created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all().values('id', 'username', 'email')
        return Response(users)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You have accessed a protected route!'})
