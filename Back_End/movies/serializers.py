from rest_framework import serializers
from django.db.models import Avg
from users.models import FavoriteMovie
from .models import Movie, Genre, FeaturedMovie, MovieRating, HeroMovie
from .models import Actor, Director, Cast, CuratedLifeMovie

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = [
            "tmdb_id",
            "name",
            "profile_path",
        ]

class CastSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)

    class Meta:
        model = Cast
        fields = [
            "actor",        # ⭐ 배우 정보
            "character",    # ⭐ 배역
            "order",
        ]


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ("tmdb_id", "name", "profile_path")


class MovieDetailSerializer(serializers.ModelSerializer):
    director = DirectorSerializer(read_only=True)
    actors = ActorSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = (
            "id",
            "tmdb_id",
            "title",
            "original_title",
            "overview",
            "poster_path",
            "backdrops",
            "release_date",
            "runtime",
            "tmdb_rating",
            "director",
            "actors",
        )


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
    profile_image = serializers.SerializerMethodField()
    movie_id = serializers.IntegerField(source='movie.id', read_only=True)
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    likesCount = serializers.SerializerMethodField(method_name='get_likes_count')
    isLiked = serializers.SerializerMethodField(method_name='get_is_liked')

    class Meta:
        model = MovieRating
        fields = (
            "id",
            "user_id", "username", "profile_image",
            "movie_id","movie_title",
            "rating", "comment",
            "created_at", "likesCount", "isLiked",
        )

    def get_profile_image(self, obj):
        try:
            return obj.user.userprofile.profile_image
        except:
            return "/mia5.png"

    def get_likes_count(self, obj):
        return obj.like_users.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like_users.filter(id=request.user.id).exists()
        return False

class MovieResponseSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()
    user_data = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    director = DirectorSerializer(read_only=True)  # ← 추가
    casts = CastSerializer(read_only=True, many=True)

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
            "is_liked",
            "director",  # ← 추가
            "casts",
        ]

    def get_genres(self, obj):
        return [g.name for g in obj.genres.all()]
    
    def get_comments(self, obj):
        serializer = MovieRatingSerializer(obj.ratings.all(), many=True, context=self.context)
        return serializer.data

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

    def get_is_liked(self, obj):
        """영화 목록에서도 is_liked 표시"""
        request = self.context.get('request', None)
        if not request or not request.user.is_authenticated:
            return False
        
        return FavoriteMovie.objects.filter(movie=obj, user=request.user).exists()

    def get_user_data(self, obj):
        request = self.context.get('request', None)
        if not request or not request.user.is_authenticated:
            return None

        user = request.user
        user_rating = MovieRating.objects.filter(movie=obj, user=user).first()
        is_liked = FavoriteMovie.objects.filter(movie=obj, user=request.user).exists()

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

# movies/serializers.py
class LifeMovieSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    movie = serializers.SerializerMethodField()
    review = serializers.SerializerMethodField()

    class Meta:
        model = CuratedLifeMovie
        fields = ["user", "movie", "review"]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
        }

    def get_movie(self, obj):
        return {
            "id": obj.movie.id,
            "title": obj.movie.title,
            "poster_path": obj.movie.poster_path,
        }

    def get_review(self, obj):
        rating = MovieRating.objects.filter(
            movie=obj.movie,
            user=obj.user
        ).first()

        if not rating:
            return None

        return {
            "rating": rating.rating,
            "comment": rating.comment,
        }
