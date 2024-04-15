from django.contrib import admin
from django.urls import path, include
from .views import weekly_top

urlpatterns = [
    path('top_movies/', weekly_top),
]
