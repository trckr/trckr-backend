from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.models import Task
from tasks.serializers import TaskSerializer

from .models import Project
from .serializers import ProjectSerializer


class ProjectView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = Project.objects.filter(createdBy=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class TaskProjectView(APIView):
    """
    Let's users query tasks for a specific project
    """

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        tasks = Task.objects.filter(project=project, createdBy=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
