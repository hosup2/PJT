from django.urls import path
from .views import UserRecommendView

urlpatterns = [
    path('', UserRecommendView.as_view()),
]
