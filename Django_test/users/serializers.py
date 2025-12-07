from rest_framework import serializers
from .models import UserPreference, FavoriteMovie, WatchedMovie
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = ("favorite_genres",)


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = "__all__"


class WatchedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedMovie
        fields = "__all__"

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        return user
