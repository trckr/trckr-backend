from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class InvalidateAuthTokenTest(APITestCase):
    def setUp(self):
        self.api_url = reverse('token-invalidation')
        self.test_user = User.objects.create_user('test', 'test@example.com',
                                                  'testpassword')
        self.test_token = Token.objects.create(user=self.test_user)

        # Authorize API calls with token
        auth = 'Token {0}'.format(self.test_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def test_invalidate_existing_token(self):
        '''
        Invalidate a token that already exists
        '''
        response = self.client.post(self.api_url)

        user_token_exists = Token.objects.filter(user=self.test_user).exists()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(user_token_exists)

    def test_invalidate_existing_token_twice(self):
        '''
        Try to invalidate a token twice and expect an error
        '''
        first_response = self.client.post(self.api_url)
        second_response = self.client.post(self.api_url)

        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.assertEqual(second_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalidate_without_token(self):
        '''
        Try to invalidate a non-existing token an expect an error
        '''
        Token.objects.filter(user=self.test_user).delete()
        response = self.client.post(self.api_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalidate_only_own_token(self):
        '''
        Check that the correct token gets deleted
        '''
        other_user = User.objects.create_user('other', 'othertest@example.com',
                                              'testpassword')
        Token.objects.create(user=other_user)

        response = self.client.post(self.api_url)

        user_token_exists = Token.objects.filter(user=self.test_user).exists()
        other_user_token_exists = Token.objects.filter(user=other_user).exists()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(other_user_token_exists)
        self.assertFalse(user_token_exists)
