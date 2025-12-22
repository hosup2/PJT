from django.urls import path
from .views import (
    ChatRecommendView,
    ChatSessionListView,
    ChatSessionDetailView,
    MovieFeedbackView,
)

urlpatterns = [
    path("chat/", ChatRecommendView.as_view(), name="recommend-chat"),
    path("sessions/", ChatSessionListView.as_view(), name="chat-session-list"),
    path("sessions/<int:session_id>/", ChatSessionDetailView.as_view(), name="chat-session-detail"),
    path("feedback/", MovieFeedbackView.as_view()),
]
