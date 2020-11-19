from django.shortcuts import render

# Create your views here.
def update_movie(request):

    # 영화 제목 가져오기! 네이버 평점 순 500개
    import requests
    from bs4 import BeautifulSoup
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
