from django.urls import path
from .views import (
    UserPreferenceView,
    FavoriteMovieView,
    FavoriteMovieDetailView,
    WatchedMovieView,
    MeView,
    MeUpdateView,
    MeDeleteView,
)

urlpatterns = [
    path("preferences/", UserPreferenceView.as_view()),
    path("favorites/", FavoriteMovieView.as_view()),
    path("favorites/<int:movie_id>/", FavoriteMovieDetailView.as_view()),
    path("watched/", WatchedMovieView.as_view()),
    path("me/", MeView.as_view()),
    path("me/update/", MeUpdateView.as_view()),
    path("me/delete/", MeDeleteView.as_view()),
]
