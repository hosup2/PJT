from rest_framework import serializers
from django.db.models import Avg
from .models import Movie, Genre, FeaturedMovie, MovieRating

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"

class MovieResponseSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()   # ⭐ 추가
    rating_count = serializers.SerializerMethodField() # ⭐ 추가

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "original_title",
            "poster_path",
            "release_date",
            "runtime",
            "genres",
            "overview",
            "tmdb_rating",
            "backdrops",
            "avg_rating",      # ⭐
            "rating_count",    # ⭐
            "stats",
        ]

    def get_genres(self, obj):
        return [g.name for g in obj.genres.all()]

    # ⭐ 평균 별점 계산
    def get_avg_rating(self, obj):
        avg = obj.ratings.aggregate(Avg("rating"))["rating__avg"]
        return round(avg, 1) if avg else 0

    # ⭐ 평가 개수
    def get_rating_count(self, obj):
        return obj.ratings.count()

    def get_stats(self, obj):
        return {
            "avg_rating": self.get_avg_rating(obj),
            "rating_count": self.get_rating_count(obj),
            "rating_distribution": {
                "5.0": 0,
                "4.0": 0,
                "3.0": 0,
                "2.0": 0,
                "1.0": 0,
            }
        }

    
class FeaturedMovieSerializer(serializers.ModelSerializer):
    movie = MovieResponseSerializer(read_only=True)

    class Meta:
        model = FeaturedMovie
        fields = ("id", "priority", "movie")

class MovieRatingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = MovieRating
        fields = (
            "id",
            "user",
            "rating",
            "comment",
            "created_at",
        )

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
        }
