from django.contrib.auth.models import User
from rest_framework import serializers

from .models import TimeEntry


class TimeEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeEntry
        fields = ('id',
                  'description',
                  'timeSpent',
                  'task')
