from django.shortcuts import render
from .models import Movie,Genre

# Create your views here.
def index(request):
    return render(request,'game/index.html')


def update_movie(request):

    import requests
    from bs4 import BeautifulSoup

    # movie_list : 네이버 평점 순 500개 영화 제목 저장할 리스트!
    movie_list=[]
    number=11
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
