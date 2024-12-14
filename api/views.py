from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User

@api_view(['GET'])
def get_user(request):
    return Response({"message": "API is working!"})

@api_view(['GET'])
def api_root(request):
    return Response({
        "status": "success",
        "message": "Welcome to the Gamify API",
        "version": "1.0.0"
    })
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# 
@api_view(['GET'])
def get_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all().values('id', 'username', 'email')
        return Response(users)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You have accessed a protected route!'})
