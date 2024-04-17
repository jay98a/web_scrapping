from django.urls import path
from ..views import weekly_top,upcoming_releases

urlpatterns = [
    path('top_movies/', weekly_top),
    path('upcoming_releases/', upcoming_releases)
]
