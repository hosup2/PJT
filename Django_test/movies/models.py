from django.db import models
from django.conf import settings

class Genre(models.Model):
    name = models.CharField(max_length=50)

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

    class Meta:
        # ⭐ unique_together 제거! 이제 같은 영화에 여러 리뷰 작성 가능
        # unique_together = ("user", "movie")  # 이 줄 삭제 또는 주석처리
        ordering = ["-created_at"]  # 최신순 정렬