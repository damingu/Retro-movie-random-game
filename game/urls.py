from django.urls import path
from . import views

app_name='game'
urlpatterns = [
    # main 페이지
    path('',views.index,name="index"),
    
    # 메인 게임 
    path('play_game/', views.play_game, name="play_game"),
    # 예고편 보러 가기
    path('<int:game_idx>/',views.movie_detail,name="movie_detail"),
    # 예고편 찜하기
    path('<int:movie_pk>/like/', views.like, name='like'),
    # 찜한 목록 보여주기
    path('my_movie_list/',views.my_movie_list,name="my_movie_list"),
    # 예고편에서 댓글쓰기
    path('<int:poster_idx>/comments/', views.create_comment, name='create_comment'),
    
    # admin용
    path('gameadmin/',views.gameadmin,name="gameadmin"),
    path('movie_update/',views.update_movie,name="update_movie"),

    
]
