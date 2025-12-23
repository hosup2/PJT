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


from .models import ChatRoom, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'username', 'message', 'created_at']

class ChatRoomSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    movie_poster = serializers.CharField(source='movie.poster_path', read_only=True)
    message_count = serializers.IntegerField(source='messages.count', read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'movie', 'movie_title', 'movie_poster', 'message_count', 'created_at', 'is_active']

