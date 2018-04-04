from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)
