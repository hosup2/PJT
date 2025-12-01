from django.db import models

class MovieCache(models.Model):
    tmdb_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    genres = models.JSONField(null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    actors = models.JSONField(null=True, blank=True)
    keywords = models.JSONField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
