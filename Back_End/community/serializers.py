from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment

User = get_user_model()


class SimpleUserSerializer(serializers.ModelSerializer):
    profile_image = serializers.CharField(source="userprofile.profile_image", read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "profile_image")


class CommentSerializer(serializers.ModelSerializer):
    """댓글 시리얼라이저"""
    author = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at',)
        read_only_fields = ('post', 'author')


class PostListSerializer(serializers.ModelSerializer):
    """게시글 목록용 시리얼라이저"""
    author = SimpleUserSerializer(read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'movie_id', 'movie_title', 
            'movie_poster', 'created_at', 'updated_at', 
            'comment_count', 'view_count'
        )
    
    def get_comment_count(self, obj):
        """댓글 개수 계산"""
        return obj.comments.count()


class PostDetailSerializer(serializers.ModelSerializer):
    """게시글 상세용 시리얼라이저"""
    author = SimpleUserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content', 
            'movie_id', 'movie_title', 'movie_poster',
            'created_at', 'updated_at', 'view_count',
            'comments', 'comment_count'
        )
        read_only_fields = ('author', 'view_count')
    
    def get_comment_count(self, obj):
        """댓글 개수 계산"""
        return obj.comments.count()


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """게시글 생성/수정용 시리얼라이저"""
    class Meta:
        model = Post
        fields = ('title', 'content', 'movie_id', 'movie_title', 'movie_poster')

