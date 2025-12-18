from django.urls import path
from .views import (
    ChatRecommendView,
    ChatSessionDetailView,
)

urlpatterns = [
    path("chat/", ChatRecommendView.as_view(), name="recommend-chat"),
    path("sessions/<int:session_id>/", ChatSessionDetailView.as_view(), name="chat-session-detail"),
]
