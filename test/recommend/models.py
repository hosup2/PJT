from django.db import models
from django.contrib.auth.models import User

class UserFavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmdb_movie_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserWatchedMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tmdb_movie_id = models.IntegerField()
    rating = models.IntegerField(null=True, blank=True)  # 0~5점 또는 like/dislike
    watched_at = models.DateTimeField(auto_now_add=True)

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_genres = models.JSONField(null=True, blank=True)
    favorite_directors = models.JSONField(null=True, blank=True)
    favorite_actors = models.JSONField(null=True, blank=True)
    favorite_keywords = models.JSONField(null=True, blank=True)
    summary_text = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

class RecommendationResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommended_movies = models.JSONField()  # [tmdb_id1, tmdb_id2, ...]
    algorithm_version = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
