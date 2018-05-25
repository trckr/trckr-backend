from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from time_entries.models import TimeEntry
from time_entries.serializers import TimeEntrySerializer

from .models import Task
from .serializers import TaskSerializer


class TaskView(ListCreateAPIView):
    """
    Let's users list and create tasks
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        queryset = Task.objects.filter(createdBy=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    """
    Let's users query and update tasks
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


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
        time_entries = TimeEntry.objects.filter(
            task=task, createdBy=request.user)
        serializer = TimeEntrySerializer(time_entries, many=True)
        return Response(serializer.data)
