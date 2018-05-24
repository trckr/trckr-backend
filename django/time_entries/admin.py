from django.contrib import admin
from .models import TimeEntry


class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('description', 'timeSpent', 'project')

    def project(self, obj):
        return '%s' % obj.task.project.id


admin.site.register(TimeEntry, TimeEntryAdmin)
