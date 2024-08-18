# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.user.models import User

class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a user and obtain a token
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )

        # Obtain token
        response = self.client.post(reverse('token_obtain_pair'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.user_data = {
            'email': 'updateduser@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'title': 'Mr.',
            'sex':'Male',
            'location': 'New Location',
            'is_verified': True
        }

    def test_get_user(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_post_user(self):
        response = self.client.post(reverse('user-list-create'), {
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
            'title': 'Mr.',
            'sex':'Male',
            'location': 'New Location',
            'is_verified': True
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'newuser@example.com')

    def test_put_user(self):
        self.user_data['password'] = 'updatedpassword'  # Add this line
        response = self.client.put(reverse('user-detail', kwargs={'pk': self.user.id}), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_user(self):
        response = self.client.patch(reverse('user-detail', kwargs={'pk': self.user.id}), {'location': 'Updated Location'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['location'], 'Updated Location')

    def test_delete_user(self):
        response = self.client.delete(reverse('user-detail', kwargs={'pk': self.user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
