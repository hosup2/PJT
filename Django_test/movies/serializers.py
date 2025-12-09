from rest_framework import serializers
from .models import Movie, Genre

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
            "stats",
            "tmdb_rating",
            "imdb_rating",
            "backdrops",
        ]

    def get_genres(self, obj):
        return [g.name for g in obj.genres.all()]

    def get_stats(self, obj):
        return {
            "avg_rating": round(obj.tmdb_rating / 2, 1) if obj.tmdb_rating else 0,
            "rating_count": 0,
            "rating_distribution": {
                "5.0": 0,
                "4.0": 0,
                "3.0": 0,
                "2.0": 0,
                "1.0": 0,
            }
        }