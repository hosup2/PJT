from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()

# A simple serializer for user information to avoid exposing sensitive data
class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class CommentSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('post', 'author',)


class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    # Add a field to count comments
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'comment_count')
        read_only_fields = ('author', 'comments',)

class PostListSerializer(PostSerializer):
    # For list view, we don't need the full comments list
    class Meta(PostSerializer.Meta):
        fields = ('id', 'author', 'title', 'created_at', 'updated_at', 'comment_count')

