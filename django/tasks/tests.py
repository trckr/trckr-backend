from dateutil import parser
from decimal import *
from django.contrib.auth.models import User
from django.urls import reverse
from projects.models import Project
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from time_entries.models import TimeEntry

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
                name='Test project 1',
                description='This is a test project',
                createdBy = self.test_user
                )
        self.test_project_2 = Project.objects.create(
                name='Test project 2',
                description='This is also a test project',
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
            'description': 'test@example.com',
            'project' : self.test_project.id,
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)

    def test_create_task_with_empty_name(self):
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
                self.api_url + str(Task.objects.latest('id').id) + '/',
                data,
                format='json'
                )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 1)

        task = Task.objects.latest('id')

        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['project'], data['project'])

    def test_update_task_with_empty_name(self):
        """
        Try to update a task with an empty name and expect an error
        """
        data = {
            'name': 'test',
            'description': 'test description',
            'project' : self.test_project.id,
        }

        self.client.post(self.api_url, data, format='json')

        data['name'] = ''

        response = self.client.put(
                self.api_url + str(Task.objects.latest('id').id) + '/',
                data,
                format='json'
                )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_non_existing_task(self):
        '''
        Try to get non-existing task and expect an error
        '''
        response = self.client.get(self.api_url + '1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_task_after_creation(self):
        '''
        Create task and retrieve it immediately again
        '''
        data = {
            'name': 'test',
            'description': 'test description',
            'project' : self.test_project.id,
        }

        response = self.client.post(self.api_url, data, format='json')
        response = self.client.get(self.api_url + str(response.data['id']) + '/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['project'], data['project'])

    def test_get_tasks_after_creation(self):
        '''
        Create multiple tasks and retrieve them immediately again
        '''
        data = [{
            'name': 'test 1',
            'description': 'test description 1',
            'project' : self.test_project.id,
        }, {
            'name': 'test 2',
            'description': 'test description 2',
            'project' : self.test_project_2.id,
        }]

        self.client.post(self.api_url, data[0], format='json')
        self.client.post(self.api_url, data[1], format='json')
        response = self.client.get(self.api_url)

        response.data.sort(key=lambda elem: elem['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i in range(len(data)):
            self.assertEqual(response.data[i]['name'],
                             data[i]['name'])
            self.assertEqual(response.data[i]['description'],
                             data[i]['description'])
            self.assertEqual(response.data[i]['project'],
                             data[i]['project'])


class TaskTimeEntryTest(APITestCase):
    def setUp(self):
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
        self.test_task = Task.objects.create(
                name='Test project',
                description='This is a test task',
                project = self.test_project,
                createdBy = self.test_user
                )

        self.test_time_entries = []
        self.test_time_entries.append(
            TimeEntry.objects.create(
                timeSpent=5,
                description='Description 1',
                startTime='2018-01-01 12:00',
                task=self.test_task,
                createdBy=self.test_user))
        self.test_time_entries.append(
            TimeEntry.objects.create(
                timeSpent=10,
                description='Description 2',
                startTime='2018-02-01 12:00',
                task=self.test_task,
                createdBy=self.test_user))
        self.test_time_entries.append(
            TimeEntry.objects.create(
                timeSpent=2,
                description='Description 3',
                startTime='2018-03-01 12:00',
                task=self.test_task,
                createdBy=self.test_user))

        # Authorize API calls with token
        auth = 'Token {0}'.format(self.test_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def test_get_time_entries_for_non_existing_task(self):
        '''
        Try to get time entries for non-existing task and expect an error
        '''
        response = self.client.get("/api/tasks/0/time-entries/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_time_entries_for_task(self):
        '''
        Get time entries for a specific task
        '''
        response = self.client.get("/api/tasks/" + str(self.test_task.id)
                                   + "/time-entries/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.test_time_entries))

        response.data.sort(key=lambda elem: elem['id'])

        for i in range(len(self.test_time_entries)):
            self.assertEqual(Decimal(response.data[i]['timeSpent']),
                             Decimal(self.test_time_entries[i].timeSpent))
            self.assertEqual(response.data[i]['description'],
                             self.test_time_entries[i].description)
            self.assertEqual(parser.parse(response.data[i]['startTime']),
                             parser.parse(self.test_time_entries[i].startTime))
            self.assertEqual(response.data[i]['task'],
                             self.test_time_entries[i].task.id)
