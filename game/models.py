from django.db import models
#from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField(null=True)
    popularity = models.FloatField(null=True)
    revenue = models.IntegerField(null=True)
    vote_average = models.FloatField(null=True)
    overview = models.TextField(null=True)
    poster_path = models.CharField(null=True,max_length=500)
    genres = models.ManyToManyField(Genre)
    #like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
