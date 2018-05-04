from django.contrib.auth.models import User
from rest_framework import serializers

from .models import TimeEntry


class TimeEntrySerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()

    def get_project(self, obj):
        return obj.task.project.id

    class Meta:
        model = TimeEntry
        fields = ('id',
                  'description',
                  'timeSpent',
                  'task',
                  'project')
