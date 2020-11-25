# 영화 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie,Genre,TempMovie
from articles import models as articles_models

from .forms import CommentForm

import random
import requests
from bs4 import BeautifulSoup

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST,require_GET

# 게임
import random 


# Create your views here.
def gameadmin(request):
    if request.user.is_staff:
        return render(request,'game/gameadmin.html')
    else:
        return render(request,'game/index.html')


def index(request):
    movies = Movie.objects.all()
    random_movie = random.choice(list(movies))
    context={
        'random_movie':random_movie,
    }
    return render(request,'game/index.html',context)


# 게임 페이지로 넘어가는 함수 
@login_required
def play_game(request):
    tempmovieall = TempMovie.objects.all()
    tempmovieall.delete()
    total = []
    num = [i for i in range(1,48)]
    # 중복없이 10개 뽑기
    randomNum = random.sample(num, 10)
    # print(randomNum)
    for idx,i in enumerate(randomNum) :
        getMovie = Movie.objects.get(id=i)
        TempMovie.objects.create(poster_idx=idx,movie_id=getMovie.id)
        total.append(getMovie)
    context = {
        'movies': total,
    }

    return render(request, 'game/play_game.html', context)


# 예고편 보러가기
@login_required
def movie_detail(request,game_idx):
    tempmovie = get_object_or_404(TempMovie,poster_idx=game_idx)
    movie_pk = tempmovie.movie_id
    movie = get_object_or_404(Movie,pk=movie_pk)
    # youtube API_KEY
    API_KEYS=[
        'AIzaSyCa5YwT7EcLVanemRFiNHhpyVy64sKu7Dw',
        'AIzaSyClauhHokVFylfo5bKnc80LTnNuurpC1O8',
        'AIzaSyCdneHhIhINFW9826nIXk0OJVtSnCq_aI8',
        'AIzaSyDthd4UCpNEiZIDddiTZZNQjxDlfsLHvc8',
    ]
   
    ## 예고편 가져오기1 TMDB에서!!
    
    # TMDB에서 영화 ID 찾기
    API_KEY = 'be806e5cce014657ffa0b51002fc8512'
    url = 'https://api.themoviedb.org/3/search/movie?api_key='+API_KEY+'&language=ko-KR&query='+movie.title+'&page=1&include_adult=false'
    res = requests.get(url)
    # movie_dict안에 영화 아이디가 있어요.
    movie_dict = res.json()
    movie_id = (movie_dict.get('results')[0].get('id'))

    # TMDB에서 영화 ID 기반으로 예고편 YOUTUBE ID 찾기
    url = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'/videos?api_key='+API_KEY+'&language=ko-KR'
    res = requests.get(url)
    movie_detail = res.json()
    if len(movie_detail.get('results')):
        youtube_id = movie_detail.get('results')[0].get('key')
        youtube = 'https://www.youtube.com/embed/'+str(youtube_id)+'?autoplay=1'
        print('tmdb')
    
    ## 예고편 가져오기1 YOUTUBE에서!!
    else:
        # TMDB에 영화 예고편 YOUTUBE ID 정보가 없다면 유투브에서 직접 검색해보기
        URL = 'https://www.googleapis.com/youtube/v3/search'
        for API_KEY in API_KEYS:
            params= {
                'part': 'snippet',
                'key': API_KEY,
                'q': movie.title +' 예고편',
            }
            res = requests.get(URL, params=params)
            youtube_result=res.json()

            # 유툽 API_KEY 할당량이 다 끝나서 더이상 검색해줄 수 없을 때, error 페이지로 넘어가기
            if youtube_result.get('items',0)==0:
                return render(request,'game/error.html')
            
            # 유툽에서 정상적으로 정보를 가져오면 그거 뿌려주기!
            else:
                print('youtube!')
                youtube_id = youtube_result['items'][0].get('id')['videoId']
                youtube = 'https://www.youtube.com/embed/'+str(youtube_id)+'?autoplay=1'
                break
    
    # 댓글 가져오기
    comments = movie.moviecomment_set.all()
    comment_form = CommentForm()

    context = {
        'youtube':youtube,
        'movie':movie,
        'comment_form': comment_form,
        'comments': comments,
        'poster_idx': tempmovie.poster_idx
    }
    return render(request,'game/movie_detail.html',context)


# # 영화 찜하기
@require_POST
def like(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie,pk=movie_pk)
        user = request.user

        if movie.like_user.filter(pk=user.pk).exists():

            movie.like_user.remove(user)
            is_like = False
        else:
            movie.like_user.add(user)
            is_like = True

        data = {
            'is_like':is_like,
            'like_count': movie.like_user.count(),
        }  
        return JsonResponse(data)
    return redirect('accounts:login')


# 영화 댓글 쓰기
@require_POST
def create_comment(request, poster_idx):
    tempmovie = get_object_or_404(TempMovie,poster_idx=poster_idx)
    movie_pk = tempmovie.movie_id
    movie = get_object_or_404(Movie,pk=movie_pk)

    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
        return redirect('game:movie_detail', poster_idx)
    context = {
        'comment_form': comment_form,
        'review': movie,
        'comments': movie.moviecomment_set.all(),
    }
    return render(request, 'game/movie_detail.html', context)


# 찜한 목록!!
def my_movie_list(request):
    user = request.user
    movies=user.like_movies.all()
    # writen_articles = get_object_or_404(articles_models.Article,pk=user.id)

    context={
        'movies':movies
    }
    return render(request,'game/my_movie_list.html',context)

@require_POST
def update_movie(request):

    # movie_list : 네이버 평점 순 500개 영화 제목 저장할 리스트!
    movie_list=[]
    number=2
    for i in range(1,number):
        URL = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&date=20201118&page='

        req = requests.get(URL+str(i))
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        ## CSS Selector를 통해 html요소들을 찾아낸다.
        my_titles = soup.select(
            ' td.title > div > a'
            )

        for title in my_titles:
            ## Tag안의 텍스트
            movie_list.append(title.get('title'))

    ## DB에 데이터 넣기
    API_KEY = 'be806e5cce014657ffa0b51002fc8512'
    for movie_title in movie_list:
        # tmdb에선 영화 정보를 찾으려면, 영화 아이디가 있어야함. 그래서 영화 아이디 찾기 위한 코드
        url = 'https://api.themoviedb.org/3/search/movie?api_key='+API_KEY+'&language=ko-KR&query='+movie_title+'&page=1&include_adult=false'
        res = requests.get(url)
        # movie_dict안에 영화 아이디가 있어요.
        movie_dict = res.json()

        # 그런데 영화 아이디가 존재하지 않는 경우가 발생했음! 그래서 그런 오류가 발생할 때를 대비해서
        # try / except 문법사용
        try:
            
            movie_id = (movie_dict.get('results')[0].get('id'))
            url = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'?api_key='+API_KEY+'&language=ko-KR'
            res = requests.get(url)

            # movie_detail에 내가 원하는 영화 정보가 들어있다!!
            movie_detail = res.json()

            # 본격적으로 우리가 가진 DB에 데이터 집어 넣기!
            # models.py에 정의한 Movie 가져와서 movie1 오브젝트 만들기
            movie1 = Movie(title=movie_title)
            
            import datetime
            # 모델링한 필드에 맞게 데이터 넣어주기
            movie1.release_date=datetime.datetime.strptime(movie_detail.get('release_date'),'%Y-%m-%d')
            movie1.popularity=movie_detail.get('popularity')
            movie1.revenue=movie_detail.get('revenue')
            movie1.vote_average=movie_detail.get('vote_average')
            movie1.overview=movie_detail.get('overview')
            movie1.poster_path=movie_detail.get('poster_path')

            # 디비에 저장!
            movie1.save()

            # manytomany field는 다음과 같이 .add를 해서 넣어줘야한다고 공식문서에 나와있어서, 이대로 함!
            for g in movie_detail.get('genres'):
                genre_id = g.get('id')
                movie1.genres.add(Genre.objects.get(id=genre_id))
            
            print(movie1)
        except:
            continue
    context={
        'movies':Movie.objects.all()
    }
    # 영화 업데이트했으면 그 결과 보는 페이지 하나 만들었어요.
    return render(request,'game/update_movie.html',context)







    '''
    ##영화 네이버 api 검색 후 DB에 저장
    for movie_tite in movie_list:
        keyword = director+' '+title
        client_id = "9iYbqEfGQkmbMGaqjtwk"
        client_secret = "o9q41jvoQy"
        url = "https://openapi.naver.com/v1/search/movie.json?query=" + keyword # json 결과
        result = requests.get(urlparse(url).geturl(),
                        headers={"X-Naver-Client-Id":client_id,
                                "X-Naver-Client-Secret":client_secret})
        movie_dict = result.json()
    print(movie_dict.get('items')[0])
    print(movie_dict.get('items')[0].get('image'))
    print(movie_dict.get('items')[0].get('director').split('|'))
    print(movie_dict.get('items')[0].get('actor').split('|'))


    

    # tmdb
    API_KEY = 'be806e5cce014657ffa0b51002fc8512'
    url = 'https://api.themoviedb.org/3/search/movie?api_key='+API_KEY+'&language=ko-KR&query='+keyword+'&page=1&include_adult=false'
    res = requests.get(url)
    movie_dict = res.json()
    movie_id = (movie_dict.get('results')[0].get('id'))

    print(movie_id)
    url = 'https://api.themoviedb.org/3/movie/'+str(movie_id)+'?api_key='+API_KEY+'&language=ko-KR'
    res = requests.get(url)
    movie_img = res.json()
    print(movie_img)
    '''
