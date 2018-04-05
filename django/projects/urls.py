from django.urls import path

from . import views

urlpatterns = [
    path('', views.ProjectView.as_view()),
    path(r'<pk>/', views.ProjectDetailView.as_view()),
    path(r'<pk>/tasks', views.TaskProjectView.as_view(), name='project-tasks'),
]
