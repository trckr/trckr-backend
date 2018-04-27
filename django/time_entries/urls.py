from django.urls import path

from . import views

urlpatterns = [
    path('', views.TimeEntryView.as_view(), name='time_entries'),
    path(r'<pk>/', views.TimeEntryDetailView.as_view(), name='time_entries-detail')
]
