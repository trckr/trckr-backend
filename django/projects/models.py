from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT)
    createDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)
