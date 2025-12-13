from rest_framework import serializers
from django.db import models
from django.contrib.auth import get_user_model
from .models import UserPreference, FavoriteMovie, WatchedMovie, UserFollow
from movies.serializers import MovieResponseSerializer


User = get_user_model()


class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ("favorite_genres",)


class FavoriteMovieSerializer(serializers.ModelSerializer):
    movie = MovieResponseSerializer(read_only=True)

    class Meta:
        model = FavoriteMovie
        fields = ("id", "movie", "created_at")


class WatchedMovieSerializer(serializers.ModelSerializer):
    movie = MovieResponseSerializer(read_only=True)

    class Meta:
        model = WatchedMovie
        fields = ("id", "movie", "watched_at")


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "비밀번호가 일치하지 않습니다."}
            )
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user

class PublicUserProfileSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    follow_info = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "stats", "follow_info")

    def get_follow_info(self, obj):
        request = self.context.get("request")

        is_following = False
        if request and request.user.is_authenticated:
            is_following = obj.followers.filter(
                follower=request.user
            ).exists()

        return {
            "followers_count": obj.followers.count(),
            "following_count": obj.following.count(),
            "is_following": is_following
        }


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ("id", "follower", "following", "created_at")
        read_only_fields = ("follower",)
