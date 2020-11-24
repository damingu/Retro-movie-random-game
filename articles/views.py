from django.shortcuts import render,redirect,get_object_or_404
from .forms import ArticleForm,CommentForm
from .models import Article, Comment
from game import models as game_models

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST,require_GET

from django.db.models import Q
# Create your views here.
def index(request):
    articles = Article.objects.filter(rating__gte=5)
    poster_path =[]
    for article in articles:
        print(article.movie.poster_path)
    context = {
        'articles1':articles[:3],
        'articles2':articles[3:],
    }
    
    return render(request,'articles/index.html',context)


def create(request,movie_pk):
    movie = get_object_or_404(game_models.Movie, pk=movie_pk)
    if request.method=='POST':
        form = ArticleForm(request.POST,request.FILES)
        if form.is_valid():
            article=form.save(commit=False)
            article.user = request.user
            article.movie = movie
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context={
        'form':form,
    }
    return render(request,'articles/form.html',context)


def detail(request,article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context={
        'article':article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request,'articles/detail.html',context)


def update(request, article_pk):
    article = get_object_or_404(Article,pk=article_pk)
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/form.html', context)


def delete(request, article_pk):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=article_pk)
        if request.user == article.user:
            article.delete()
            return redirect('articles:index')
    return redirect('articles:detail', article.pk)


def create_comment(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()
        return redirect('articles:detail', article.pk)
    context = {
        'comment_form': comment_form,
        'review': article,
        'comments': article.comment_set.all(),
    }
    return render(request, 'articles/detail.html', context)


# def like(request, article_pk):
#     if request.user.is_authenticated:
#         article = get_object_or_404(Article, pk=article_pk)
#         user = request.user

#         if article.like_users.filter(pk=user.pk).exists():
#             article.like_users.remove(user)
#             is_like=False
#         else:
#             article.like_users.add(user)
#             is_like=True
#         data = {
#             'is_like':is_like,
#             'like_count': article.like_users.count(),
#         }
#         return JsonResponse(data)
#     return redirect('accounts:login')