from datetime import datetime
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from tasks.models import Task


class TimeEntry(models.Model):
    description = models.TextField(blank=True, default="")
    startTime = models.DateTimeField(default=datetime.now, blank=True)
    timeSpent = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        validators=[MinValueValidator(Decimal('0.01'))])

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    createdBy = models.ForeignKey(User, on_delete=models.PROTECT)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)
