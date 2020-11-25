from django.shortcuts import render,redirect,get_object_or_404
from .forms import ArticleForm,CommentForm
from .models import Article, Comment
from game import models as game_models

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods,require_POST,require_GET

from django.db.models import Q

from django.http import JsonResponse
# Create your views here.
def index(request):
    real_articles = Article.objects.all().order_by('-pk')
    
    # 좋아요 많은거 순으로 보여주기!
    rank_data = {}
    for a in real_articles:
        rank_data[a.pk]=len(a.like_user.all())
    rank_data=sorted(rank_data.items(),reverse=True,key=lambda item: item[1])[:8]
    rank_articles = []
    for id,_ in rank_data:
        rank_articles.append(get_object_or_404(Article,pk=id))

    context = {
        'articles1':rank_articles[:4],
        'articles2':rank_articles[4:8],
        'real_articles':real_articles,
    }
    return render(request,'articles/index.html',context)

@login_required
@require_http_methods(['GET', 'POST'])
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


@login_required
@require_http_methods(['GET', 'POST'])
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


@require_POST
def delete(request, article_pk):
    if request.user.is_authenticated:
        article = Article.objects.get(pk=article_pk)
        if request.user == article.user:
            article.delete()
            return redirect('articles:index')
    return redirect('articles:detail', article.pk)


@require_POST
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


@require_POST
def comments_delete(request, article_pk, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:detail', article_pk)


@require_POST
def like(request, article_pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=article_pk)
        user = request.user
        
        if article.like_user.filter(pk=user.pk).exists():
            article.like_user.remove(user)
            is_like=False
        else:
            article.like_user.add(user)
            is_like=True
        data = {
            'is_like':is_like,
            'like_count': article.like_user.count(),
        }
        return JsonResponse(data)
    return redirect('accounts:login')