from django.urls import path
from .views import get_user
from .views import CustomTokenObtainPairView, RegisterView, ProtectedView

urlpatterns = [
    path('users/', get_user, name='get_user'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]