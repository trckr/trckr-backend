from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework_jwt import utils
from tasks.models import Task


from .models import Project

class TaskProjectTest(APITestCase):
    def setUp(self):
        # TODO: find out how to use reverse with
        # params in the url
        #self.api_url = reverse('project-tasks')
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

        self.test_tasks = []
        self.test_tasks.append(Task.objects.create(
                name='Task 1',
                description='Description 1',
                project = self.test_project,
                createdBy = self.test_user
                ))
        self.test_tasks.append(Task.objects.create(
                name='Task 2',
                description='Description 2',
                project = self.test_project,
                createdBy = self.test_user
                ))
        self.test_tasks.append(Task.objects.create(
                name='Task 3',
                description='Description 3',
                project = self.test_project,
                createdBy = self.test_user
                ))

        # Authorize API calls with token
        payload = utils.jwt_payload_handler(self.test_user)
        token = utils.jwt_encode_handler(payload)
        auth = 'JWT {0}'.format(token)
        self.client.credentials(HTTP_AUTHORIZATION=auth)

    def test_get_tasks_for_nonexisting_project(self):
        response = self.client.get("/api/project/0/tasks")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_tasks_for_project(self):
        response = self.client.get(
                "/api/project/" + str(self.test_project.id) + "/tasks"
                )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.test_tasks))

        response.data.sort(key=lambda elem: elem['id'])

        for i in range(len(self.test_tasks)):
            self.assertEqual(response.data[i]['name'],
                             self.test_tasks[i].name)
            self.assertEqual(response.data[i]['description'],
                             self.test_tasks[i].description)
            self.assertEqual(response.data[i]['project'],
                             self.test_tasks[i].project.id)
