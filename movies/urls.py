from django.urls import path

app_name="movies"
urlpatterns = [
    path('updateMovie/',views.update_movie,name="update_movie"),
]
