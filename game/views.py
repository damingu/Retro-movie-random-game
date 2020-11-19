from django.shortcuts import render
from . import models

# Create your views here.
def update_movie(request):

    # 영화 제목 가져오기! 네이버 평점 순 500개
    import requests
    from bs4 import BeautifulSoup

    # 영화 제목!
    movie_list=[]
    for i in range(1,3):
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

    # 영화 네이버 api 검색 후 DB에 저장
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


    models.Movie.objects.create()

    ## tmdb
    '''
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
