from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    createdBy = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ('id',
                  'name',
                  'description',
                  'project',
                  'createdBy')
        
        read_only_fields = ('createdBy', )
