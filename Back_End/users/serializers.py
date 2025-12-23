from rest_framework import serializers
from django.db import models
from django.contrib.auth import get_user_model
from .models import UserPreference, FavoriteMovie, WatchedMovie, UserFollow, UserProfile
from movies.serializers import MovieResponseSerializer, MovieRatingSerializer


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
    profile_image = serializers.CharField(
        source="userprofile.profile_image",
        read_only=True
    )

    class Meta:
        model = User
        fields = ("id", "username", "email", "profile_image")




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

from movies.models import MovieRating
from django.db.models import Avg, Count
from django.db.models.functions import Coalesce


class PublicUserProfileSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    follow_info = serializers.SerializerMethodField()
    rated_movies = serializers.SerializerMethodField()
    liked_movies = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id", "username", "stats", "follow_info", "rated_movies", "liked_movies", "reviews", "profile_image")

    def get_stats(self, obj):
        # obj is the user instance
        ratings = MovieRating.objects.filter(user=obj)
        
        # Coalesce is used to ensure we get 0 instead of None for users with no ratings
        avg_rating = ratings.aggregate(avg=Coalesce(Avg('rating'), 0.0))['avg']
        
        total_ratings = ratings.count()
        total_comments = ratings.filter(comment__isnull=False).exclude(comment__exact='').count()
        
        liked_movies_count = FavoriteMovie.objects.filter(user=obj).count()
        
        return {
            'total_ratings': total_ratings,
            'avg_rating': avg_rating,
            'liked_movies': liked_movies_count,
            'total_comments': total_comments
        }

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

    def get_rated_movies(self, obj):
        ratings = MovieRating.objects.filter(user=obj).select_related('movie')
        return [{
            'id': rating.id,
            'movie_id': rating.movie.id,
            'title': rating.movie.title,
            'poster_path': rating.movie.poster_path,
            'rating': rating.rating,
        } for rating in ratings if rating.rating is not None]

    def get_liked_movies(self, obj):
        liked_movies = FavoriteMovie.objects.filter(user=obj).select_related('movie')
        return [{
            'id': fav.movie.id,
            'title': fav.movie.title,
            'poster_path': fav.movie.poster_path,
            'release_date': str(fav.movie.release_date) if fav.movie.release_date else None,
        } for fav in liked_movies]

    def get_reviews(self, obj):
        reviews = MovieRating.objects.filter(user=obj, comment__isnull=False).exclude(comment__exact='').select_related('movie')
        return MovieRatingSerializer(reviews, many=True, context=self.context).data

    def get_profile_image(self, obj):
        try:
            return obj.userprofile.profile_image
        except UserProfile.DoesNotExist:
            return "/mia5.png"

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = ("id", "follower", "following", "created_at")
        read_only_fields = ("follower",)