from django.urls import path
from . import views

app_name='game'
urlpatterns = [
    # admin용
    path('gameadmin/',views.gameadmin,name="gameadmin"),
    # 영화 랜덤해주는 곳
    path('',views.index,name="index"),
    # 예고편 보러 가기
    path('<int:movie_pk>/',views.movie_detail,name="movie_detail"),
    # 예고편 찜하기
    path('<int:movie_pk>/like/', views.like, name='like'),
    # 예고편에서 댓글쓰기
    path('<int:movie_pk>/comments/', views.create_comment, name='create_comment'),


    path('movie_update/',views.update_movie,name="update_movie"),
    path('my_movie_list/',views.my_movie_list,name="my_movie_list"),
]
