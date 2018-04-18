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
        auth = 'Token {0}'.format(self.test_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def test_create_task(self):
        """
        Create a new task
        """
        data = {
            'name': 'test',
            'description': 'test description',
            'project' : self.test_project.id,
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.latest('id')

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['project'], data['project'])

    def test_create_task_without_name(self):
        """
        Cannot create a task without a name
        """
        data = {
            'name': '',
            'description': 'test@example.com',
            'project' : self.test_project.id,
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)

    def test_update_task(self):
        """
        Updates a task
        """
        data = {
            'name': 'test',
            'description': 'test description',
            'project' : self.test_project.id,
        }

        self.client.post(self.api_url, data, format='json')

        data['description'] = 'updated description'

        response = self.client.put(
                self.api_url + str(Task.objects.latest('id').id),
                data,
                format='json'
                )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.latest('id')

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['project'], data['project'])

    def test_update_task_with_no_name(self):
        """
        Updates a task
        """
        data = {
            'name': 'test',
            'description': 'test description',
            'project' : self.test_project.id,
        }

        self.client.post(self.api_url, data, format='json')

        data['name'] = ''

        response = self.client.put(
                self.api_url + str(Task.objects.latest('id').id),
                data,
                format='json'
                )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexisting_task(self):
        response = self.client.get(self.api_url + "1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_task_after_creation(self):
        data = {
            'name': 'test',
            'description': 'test description',
            'project' : self.test_project.id,
        }

        response = self.client.post(self.api_url, data, format='json')
        response = self.client.get(self.api_url + str(response.data['id']))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['project'], data['project'])
