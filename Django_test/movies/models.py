from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    overview = models.TextField()
    poster_path = models.CharField(max_length=200, null=True)
    release_date = models.DateField(null=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title
