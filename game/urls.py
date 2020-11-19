from django.urls import path
from . import views

app_name='game'
urlpatterns = [
    path('movie_update/',views.update_movie,name="update_movie"),

]
