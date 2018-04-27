from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from time_entries.models import TimeEntry
from time_entries.serializers import TimeEntrySerializer

from .models import Task
from .serializers import TaskSerializer


class TaskView(APIView):
    """
    Let's users create new tasks
    """

    def post(self, request, format='json'):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['createdBy'] = request.user
            task = serializer.save()
            if task:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    """
    Let's users query and update tasks
    """

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format='json'):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskTimeEntryView(APIView):
    """
    Let's users query time entries for a specific task
    """

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        time_entries = TimeEntry.objects.filter(task=task, createdBy=request.user)
        serializer = TimeEntrySerializer(time_entries, many=True)
        return Response(serializer.data)
