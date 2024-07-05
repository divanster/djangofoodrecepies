# api/tests/test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User

class PublicUserApiTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_create_user_success(self):
        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(self.register_url, payload, format='json')

        print(f"Status Code: {res.status_code}")
        print(f"Response Content: {res.content}")
        print(f"Response JSON: {res.json()}")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
