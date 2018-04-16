from django.contrib import admin
from .models import TimeEntry

class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('description', 'timeSpent')


admin.site.register(TimeEntry, TimeEntryAdmin)
