from django.db import models
from django.conf import settings

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)  # TMDB genre id
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Actor(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Director(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    profile_path = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)

    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, null=True, blank=True)

    overview = models.TextField()

    poster_path = models.CharField(max_length=200, null=True, blank=True)
    backdrops = models.CharField(max_length=200, null=True, blank=True)

    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)

    tmdb_rating = models.FloatField(null=True, blank=True)
    
    genres = models.ManyToManyField(Genre)

        # ✅ 추가
    director = models.ForeignKey(
        Director,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="movies",
    )
    actors = models.ManyToManyField(
        Actor,
        blank=True,
        related_name="movies",
    )

class Cast(models.Model):
    movie = models.ForeignKey(
        Movie,
        related_name="casts",
        on_delete=models.CASCADE
    )
    actor = models.ForeignKey(      # ⭐ FK
        Actor,
        null=True,                  # ⭐ 중요
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cast_roles"
    )
    
    character = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=99)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} as {self.character}"


class FeaturedMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="featured_items")
    priority = models.IntegerField(default=0)  # 배너에 보이는 순서
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["priority", "-created_at"]  # priority → 최신순
        verbose_name = "Featured Movie"
        verbose_name_plural = "Featured Movies"

    def __str__(self):
        return f"{self.priority} - {self.movie.title}"


class MovieRating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="movie_ratings"
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    rating = models.FloatField(null=True, blank=True)  # ⭐ null=True 추가 (평점 없이 댓글만 가능)
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="comment_likes",
        blank=True
    )

    class Meta:
        # ⭐ unique_together 제거! 이제 같은 영화에 여러 리뷰 작성 가능
        unique_together = ("user", "movie")  # 이 줄 삭제 또는 주석처리
        ordering = ["-created_at"]  # 최신순 정렬


class HeroMovie(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="hero_items"
    )
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    keyword = models.CharField(
        max_length=50,
        blank=True,
        help_text="예: 개봉임박, 오스카 수상, 평론가 극찬"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["priority", "-updated_at"]

    def __str__(self):
        return f"{self.priority}. {self.movie.title}"

# movies/models.py
class CuratedLifeMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(default=0)  # 노출 순서
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["priority"]
