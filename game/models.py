from django.db import models

# Create your models here.
class Movie(models.Model):
    movieId = models.IntegerField()
    title = models.TextField()
    overview = models.TextField()
    rating = models.FloatField()
    poster_path=models.TextField()

class Genre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    name = models.TextField()

class Actor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    name = models.TextField()
