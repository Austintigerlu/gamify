from django.test import TestCase

import os
import sys

import site

# Add virtual environment's site-packages to Python path
site_packages_path = '/Users/phoelandsiu/gamify/myenv/lib/python3.10/site-packages'
if site_packages_path not in sys.path:
    sys.path.append(site_packages_path)

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamify.settings')

# Initialize Django
import django
django.setup()


# Create your tests here.
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class JWTAuthTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")

    def test_token_generation(self):
        response = self.client.post('/gamify/api/token/', {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        print("Test Passed: Token generation works!")

    def test_register(self):
        response = self.client.post(
            '/gamify/api/register/', 
            {
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'newpassword123'
            }
        )
        self.assertEqual(response.status_code, 201)  # HTTP 201 Created
        self.assertIn('message', response.data)  # Check if the success message is present
        self.assertEqual(response.data['message'], 'User created successfully')  # Verify the response message
        print("Test Passed: Register endpoint works!")


    def test_protected_route(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/gamify/api/protected/')
        self.assertEqual(response.status_code, 200)
        print("Test Passed: Protected route works!")