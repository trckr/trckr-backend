from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class AccountsTest(APITestCase):
    def setUp(self):
        self.api_url = reverse('account-create')

    def test_create_user(self):
        """
        Create a new user and check if a token is returned
        """
        data = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Max',
            'last_name': 'Muster'
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.latest('id')
        token = Token.objects.get(user=user)

        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertFalse('password' in response.data) # We don't return the password
        self.assertEqual(response.data['token'], token.key)

    def test_create_user_with_too_short_password(self):
        """
        Try creating a user with a too short password
        and check if 400 error code is returned
        """
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password': 'test',
                'first_name': 'Max',
                'last_name': 'Muster'
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_password(self):
        """
        Try creating a user with a no password
        and check if 400 error code is returned
        """
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password': '',
                'first_name': 'Max',
                'last_name': 'Muster'
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_username(self):
        """
        Try creating a user with a no username
        and check if 400 error code is returned
        """
        data = {
                'username': '',
                'email': 'test@example.com',
                'password': 'testpassword',
                'first_name': 'Max',
                'last_name': 'Muster'
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_existing_username(self):
        """
        Try creating a user with an existing username
        and check if 400 error code is returned
        """
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password': 'testpassword',
                'first_name': 'Max',
                'last_name': 'Muster'
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_firstname(self):
        """
        Try creating a user with a no first name
        and check if 400 error code is returned
        """
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password': 'testpassword',
                'first_name': '',
                'last_name': 'Muster'
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_lastname(self):
        """
        Try creating a user with a no last name
        and check if 400 error code is returned
        """
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password': 'testpassword',
                'first_name': 'Max',
                'last_name': ''
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
