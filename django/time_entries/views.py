from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TimeEntry
from .serializers import TimeEntrySerializer


class TimeEntryView(APIView):
    """
    Let's users create new time entries for tasks
    """

    def post(self, request, format='json'):
        serializer = TimeEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['createdBy'] = request.user
            time_entry = serializer.save()
            if time_entry:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        time_entries = TimeEntry.objects.filter(createdBy=request.user)
        serializer = TimeEntrySerializer(time_entries, many=True)
        return Response(serializer.data)

class TimeEntryDetailView(APIView):
    """
    Let's users query and update time entries
    """

    def get_object(self, pk):
        try:
            return TimeEntry.objects.get(pk=pk)
        except TimeEntry.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        time_entry = self.get_object(pk)
        serializer = TimeEntrySerializer(time_entry)
        return Response(serializer.data)

    def put(self, request, pk, format='json'):
        time_entry = self.get_object(pk)
        serializer = TimeEntrySerializer(time_entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
