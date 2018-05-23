from django.urls import path

from . import views

urlpatterns = [
    path('', views.TaskView.as_view(), name='tasks'),
    path(r'<pk>/', views.TaskDetailView.as_view(), name='tasks-detail'),
    path(r'<pk>/time-entries/', views.TaskTimeEntryView.as_view(), name='tasks-time-entries')
]
