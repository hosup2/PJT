from django.urls import path
from .views import (
    UserPreferenceView,
    FavoriteMovieView,
    FavoriteMovieDetailView,
    WatchedMovieView,
    MeView,
    MeUpdateView,
    MeDeleteView,
    SignupView,
    UserProfileView,
    UserReviewListView,
    FollowToggleView,
    FollowerListView,
    FollowingListView,
)

urlpatterns = [
    path("preferences/", UserPreferenceView.as_view()),
    path("favorites/", FavoriteMovieView.as_view()),
    path("favorites/<int:movie_id>/", FavoriteMovieDetailView.as_view()),
    path("watched/", WatchedMovieView.as_view()),
    path("me/", MeView.as_view()),
    path("me/update/", MeUpdateView.as_view()),
    path("me/delete/", MeDeleteView.as_view()),
    path("signup/", SignupView.as_view()),
    path("<int:user_id>/profile/", UserProfileView.as_view()),
    path("<int:user_id>/reviews/", UserReviewListView.as_view()),
    path("<int:user_id>/follow/", FollowToggleView.as_view()),
    path("<int:user_id>/followers/", FollowerListView.as_view()),
    path("<int:user_id>/following/", FollowingListView.as_view()),

]
