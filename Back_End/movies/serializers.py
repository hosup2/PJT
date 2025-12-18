from rest_framework import serializers
from django.db.models import Avg
from rest_framework import serializers
from django.db.models import Avg
from users.models import FavoriteMovie
from .models import Movie, Genre, FeaturedMovie, MovieRating, HeroMovie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = "__all__"

class MovieRatingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    profile_image = serializers.ImageField(source='user.profile_image', read_only=True)
    review_content = serializers.CharField(source='comment', read_only=True)
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = MovieRating
        fields = (
            "id",
            "user_id", "username", "profile_image",
            "movie_id","movie_title",
            "rating", "comment", "review_content",
            "created_at", "likes_count", "is_liked",
        )

    def get_likes_count(self, obj):
        # Placeholder
        return 0

    def get_is_liked(self, obj):
        # Placeholder
        return False

class MovieResponseSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()
    comments = MovieRatingSerializer(source='ratings', many=True, read_only=True)

    class Meta:
        model = Movie
        fields = [
            "id",
            "tmdb_id",
            "title",
            "original_title",
            "poster_path",
            "release_date",
            "runtime",
            "genres",
            "overview",
            "tmdb_rating",
            "backdrops",
            "stats",
            "user_data",
            "comments",
        ]

    def get_genres(self, obj):
        return [g.name for g in obj.genres.all()]

    def get_stats(self, obj):
        ratings = obj.ratings.all()
        
        # None이 아닌 rating만 필터링
        valid_ratings = [r for r in ratings if r.rating is not None]
        
        # 평균 계산
        if valid_ratings:
            avg = sum(r.rating for r in valid_ratings) / len(valid_ratings)
        else:
            avg = 0
        
        # 분포 계산
        distribution = {f"{i}.0": 0 for i in range(1, 6)}
        for r in valid_ratings:
            try:
                key = f"{int(r.rating)}.0"
                if key in distribution:
                    distribution[key] += 1
            except (ValueError, TypeError):
                continue
        
        return {
            "avg_rating": round(avg, 1) if avg else 0,
            "rating_count": len(valid_ratings),
            "rating_distribution": distribution
        }

    def get_user_data(self, obj):
        request = self.context.get('request', None)
        if not request or not request.user.is_authenticated:
            return None

        user = request.user
        user_rating = MovieRating.objects.filter(movie=obj, user=user).first()
        is_liked = FavoriteMovie.objects.filter(movie=obj, user=user).exists()

        return {
            'rating': user_rating.rating if user_rating else 0,
            'comment': user_rating.comment if user_rating else "",
            'is_liked': is_liked,
        }

    
class FeaturedMovieSerializer(serializers.ModelSerializer):
    movie = MovieResponseSerializer(read_only=True)

    class Meta:
        model = FeaturedMovie
        fields = ("id", "priority", "movie")


class HeroMovieSerializer(serializers.ModelSerializer):
    movie = MovieResponseSerializer(read_only=True)

    class Meta:
        model = HeroMovie
        fields = ("id", "priority", "keyword", "movie")
