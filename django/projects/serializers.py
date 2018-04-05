from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    createdBy = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'modifiedDate', 'createdDate', 'createdBy')
        read_only_fields = ('createdBy',)
