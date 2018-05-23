from dateutil import parser
from decimal import *
from django.contrib.auth.models import User
from django.urls import reverse
from projects.models import Project
from tasks.models import Task
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .models import TimeEntry

class TimeEntryTest(APITestCase):

    def setUp(self):

        self.api_url = reverse('time_entries')
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

        # Authorize API calls with token
        auth = 'Token {0}'.format(self.test_token)
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def test_create_time_entry(self):
        data = {
            'description': 'test description',
            'startTime' : '2018-01-01 12:00',
            'timeSpent' : 1.25,
            'task' : self.test_task.id,
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TimeEntry.objects.count(), 1)

        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(parser.parse(response.data['startTime']),
                         parser.parse(data['startTime']))
        self.assertEqual(Decimal(response.data['timeSpent']),
                         Decimal(data['timeSpent']))
        self.assertEqual(response.data['task'], data['task'])

    def test_create_time_entry_without_start_time(self):
        data = {
            'description': 'test description',
            'timeSpent' : 1.25,
            'task' : self.test_task.id,
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TimeEntry.objects.count(), 1)

        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(Decimal(response.data['timeSpent']),
                         Decimal(data['timeSpent']))
        self.assertEqual(response.data['task'], data['task'])

    def test_create_time_entry_with_zero_time(self):
        data = {
            'description': 'test description',
            'startTime' : '2018-01-01 12:00',
            'timeSpent' : 0,
            'task' : self.test_task.id,
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TimeEntry.objects.count(), 0)

    def test_create_time_entry_with_negative_time(self):
        data = {
            'description': 'test description',
            'startTime' : '2018-01-01 12:00',
            'timeSpent' : -5,
            'task' : self.test_task.id,
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TimeEntry.objects.count(), 0)

    def test_create_time_entry_with_negative_time(self):
        data = {
            'description': 'test description',
            'startTime' : '2018-01-01 12:00',
            'timeSpent' : -5,
            'task' : self.test_task.id,
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TimeEntry.objects.count(), 0)

    def test_create_time_entry_with_no_task(self):
        data = {
            'description': 'test description',
            'startTime' : '2018-01-01 12:00',
            'timeSpent' : 1
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TimeEntry.objects.count(), 0)

    def test_create_time_entry_with_for_non_existing_task(self):
        data = {
            'description': 'test description',
            'startTime' : '2018-01-01 12:00',
            'timeSpent' : 1,
            'task' : 0
        }

        response = self.client.post(self.api_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TimeEntry.objects.count(), 0)

    def test_update_time_entry(self):
        data = {
            'description': 'test description',
            'startTime' : '2018-01-01 12:00',
            'timeSpent' : 1.25,
            'task' : self.test_task.id,
        }

        self.client.post(self.api_url, data, format='json')

        data['description'] = 'updated description'
        data['startTime'] = '2018-01-01 12:00'

        response = self.client.put(
                self.api_url + str(TimeEntry.objects.latest('id').id) + '/',
                data,
                format='json'
                )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TimeEntry.objects.count(), 1)

        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(parser.parse(response.data['startTime']),
                         parser.parse(data['startTime']))
        self.assertEqual(Decimal(response.data['timeSpent']),
                         Decimal(data['timeSpent']))
        self.assertEqual(response.data['task'], data['task'])

    def test_get_nonexisting_time_entry(self):
        response = self.client.get(self.api_url + '1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_time_entry_after_creation(self):
        data = {
            'description': 'test description',
            'startTime' : '2018-01-01 12:00',
            'timeSpent' : 1.25,
            'task' : self.test_task.id,
        }

        response = self.client.post(self.api_url, data, format='json')
        response = self.client.get(self.api_url + str(response.data['id']) + '/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(parser.parse(response.data['startTime']),
                         parser.parse(data['startTime']))
        self.assertEqual(Decimal(response.data['timeSpent']),
                         Decimal(data['timeSpent']))
        self.assertEqual(response.data['task'], data['task'])

    def test_get_own_time_entries(self):
        data = {
            'description': 'test description',
            'startTime' : '2018-01-01 12:00',
            'timeSpent' : 1.25,
            'task' : self.test_task.id,
        }
        response = self.client.post(self.api_url, data, format='json')
        response = self.client.get(self.api_url)

        self.assertEqual(TimeEntry.objects.count(), 1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['description'], data['description'])
        self.assertEqual(parser.parse(response.data[0]['startTime']),
                         parser.parse(data['startTime']))
        self.assertEqual(Decimal(response.data[0]['timeSpent']),
                         Decimal(data['timeSpent']))
        self.assertEqual(response.data[0]['task'], data['task'])
