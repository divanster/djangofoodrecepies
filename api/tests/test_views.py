# api/tests/test_views.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User


class PublicUserApiTests(APITestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse('api-register')  # Ensure this matches the name in urls.py

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }
        res = self.client.post(self.create_user_url, payload, format='json')

        # Debugging output
        print(f"Status Code: {res.status_code}")
        print(f"Response Content: {res.content}")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(username=payload['username'])
        self.assertTrue(user)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
