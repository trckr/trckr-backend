from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectView.as_view(), name='projects'),
    path(r'<pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path(r'<pk>/tasks', views.TaskProjectView.as_view(), name='project-tasks'),
]
