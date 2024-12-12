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