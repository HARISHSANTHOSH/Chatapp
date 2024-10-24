from django.urls import path

from . import views

urlpatterns = [
    # Add at least one URL pattern here
    path("", views.index, name="index"),  # Example pattern
    # Add more patterns as needed
]
