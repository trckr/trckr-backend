from django.contrib.auth.models import User
from django.urls import reverse
from projects.models import Project
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework_jwt import utils

from .models import Task


class TasksTest(APITestCase):
    def setUp(self):
        self.api_url = reverse('tasks')
        self.test_user = User.objects.create_user(
                'test',
                'test@example.com',
                'testpassword'
                )
        self.test_token = Token.objects.create(user=self.test_user)
        self.test_project = Project.objects.create(
                name='Test project',
                description='This is a test project',
                createdBy = self.test_user
                )
        self.test_project = Project.objects.create(
                name='Test project',
                description='This is a test project',
                createdBy = self.test_user
                )

        # Authorize API calls with token
        payload = utils.jwt_payload_handler(self.test_user)
        token = utils.jwt_encode_handler(payload)
        auth = 'JWT {0}'.format(token)
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def test_create_task(self):
        """
        Create a new task
        """
        data = {
            'name': 'test',
            'description': 'test@example.com',
            'project' : self.test_project.id,
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.latest('id')

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['project'], data['project'])
