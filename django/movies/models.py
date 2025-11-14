from django.db import models

# Create your models here.
class Actor(models.Model):
    name = models.TextField()

class Movie(models.Model):
    title = models.TextField()
    overview = models.TextField()
    release_date = models.DateTimeField()
    poster_path = models.CharField()
    actors = models.ManyToManyField(Actor ,related_name="movies")



class Review(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    title = models.TextField()
    content = models.TextField()







