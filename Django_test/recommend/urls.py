from django.urls import path
from .views import RecommendMovieView

urlpatterns = [
    path("", RecommendMovieView.as_view()),
]
