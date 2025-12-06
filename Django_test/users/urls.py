from django.urls import path
from .views import (
    UserPreferenceView,
    FavoriteMovieView,
    FavoriteMovieDetailView,
    WatchedMovieView,
)

urlpatterns = [
    path("preferences/", UserPreferenceView.as_view()),
    path("favorites/", FavoriteMovieView.as_view()),
    path("favorites/<int:movie_id>/", FavoriteMovieDetailView.as_view()),
    path("watched/", WatchedMovieView.as_view()),
]
