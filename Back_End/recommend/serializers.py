from rest_framework import serializers
from .models import ChatSession, ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id", "role", "content", "created_at"]

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ["id", "title", "created_at", "messages"]

class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField()
    session_id = serializers.IntegerField(
        required=False,
        allow_null=True
    )

class ChatResponseSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    answer = serializers.CharField()
    movies = serializers.ListField()
