from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from tasks.models import Task

from .models import Project


class ProjectTest(APITestCase):
    def setUp(self):
        self.api_url = reverse('projects')
        self.test_user = User.objects.create_user('test', 'test@example.com',
                                                  'testpassword')
        self.test_token = Token.objects.create(user=self.test_user)
        self.test_project = Project.objects.create(
            name='existing project',
            description='This is a test project',
            createdBy=self.test_user)

        # Authorize API calls with token
        auth = 'Token {0}'.format(self.test_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def test_get_projects(self):
        """
        Get a list of projects via GET request
        """
        response = self.client.get(self.api_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_project(self):
        """
        Create a project via POST
        """
        data = {'name': 'test project', 'description': 'test description'}

        response = self.client.post(self.api_url, data, format='json')
        latest_project = Project.objects.latest('id')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], latest_project.id)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])

    def test_create_project_without_name(self):
        """
        Try to create a project without a name and get an error
        """
        data = {'description': 'test description'}

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_project_with_empty_name(self):
        """
        Try to create a project without a name and get an error
        """
        data = {'name' : '', 'description': 'test description'}

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProjectDetailTest(APITestCase):
    def setUp(self):
        self.api_url = reverse('projects')
        self.test_user = User.objects.create_user('test', 'test@example.com',
                                                  'testpassword')
        self.test_token = Token.objects.create(user=self.test_user)

        # Authorize API calls with token
        auth = 'Token {0}'.format(self.test_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def test_get_project(self):
        '''
        Get a specific project via GET request
        '''
        test_project = Project.objects.create(
            name='test project',
            description='This is a test project',
            createdBy=self.test_user)

        response = self.client.get(
            self.api_url + '{}/'.format(test_project.id), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], test_project.id)
        self.assertEqual(response.data['name'], test_project.name)

    def test_update_project(self):
        '''
        Update a project via PUT
        '''
        data = {'name': 'update project' }

        test_project = Project.objects.create(
            name='test project',
            description='This is a test project',
            createdBy=self.test_user)

        response = self.client.put(
            self.api_url + '{}/'.format(test_project.id), data, format='json')
        project_after_update = Project.objects.get(id=test_project.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(project_after_update.name, data['name'])

    def test_update_project_with_empty_name(self):
        '''
        Try to update a project with an empty name and expect an error
        '''
        data = {'name': '', }

        test_project = Project.objects.create(
            name='test project',
            description='This is a test project',
            createdBy=self.test_user)

        response = self.client.put(
            self.api_url + '{}/'.format(test_project.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_project(self):
        '''
        Delete a project via DELETE
        '''
        test_project = Project.objects.create(
            name='test project',
            description='This is a test project',
            createdBy=self.test_user)

        response = self.client.delete(
            self.api_url + '{}/'.format(test_project.id), format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Project.objects.filter(pk=test_project.id)), 0)

    def test_delete_non_existing_project(self):
        '''
        Try to delete a non-existing project and expect an error
        '''
        response = self.client.delete(
            self.api_url + '{}/'.format(0), format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TaskProjectTest(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('test', 'test@example.com',
                                                  'testpassword')
        self.test_token = Token.objects.create(user=self.test_user)
        self.test_project = Project.objects.create(
            name='Test project',
            description='This is a test project',
            createdBy=self.test_user)

        self.test_tasks = []
        self.test_tasks.append(
            Task.objects.create(
                name='Task 1',
                description='Description 1',
                project=self.test_project,
                createdBy=self.test_user))
        self.test_tasks.append(
            Task.objects.create(
                name='Task 2',
                description='Description 2',
                project=self.test_project,
                createdBy=self.test_user))
        self.test_tasks.append(
            Task.objects.create(
                name='Task 3',
                description='Description 3',
                project=self.test_project,
                createdBy=self.test_user))

        # Authorize API calls with token
        auth = 'Token  {0}'.format(self.test_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def test_get_tasks_for_non_existing_project(self):
        '''
        Try to get tasks for non-existing project and expect an error
        '''
        response = self.client.get("/api/projects/0/tasks/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_tasks_for_project(self):
        '''
        Get tasks for a specific project via GET request
        '''
        response = self.client.get("/api/projects/" + str(self.test_project.id)
                                   + "/tasks/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.test_tasks))

        response.data.sort(key=lambda elem: elem['id'])

        for i in range(len(self.test_tasks)):
            self.assertEqual(response.data[i]['name'], self.test_tasks[i].name)
            self.assertEqual(response.data[i]['description'],
                             self.test_tasks[i].description)
            self.assertEqual(response.data[i]['project'],
                             self.test_tasks[i].project.id)
