from django.urls import path

from . import views

urlpatterns = [
    path('invalidate/', views.InvalidateAuthToken.as_view(), name='token-invalidation')
]
