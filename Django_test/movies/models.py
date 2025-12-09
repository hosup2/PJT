from django.db import models

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
    imdb_rating = models.FloatField(null=True, blank=True)

    genres = models.ManyToManyField(Genre)
