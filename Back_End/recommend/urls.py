from django.urls import path
from .views import AIRecommendView

urlpatterns = [
    path("ai/", AIRecommendView.as_view()),
]
