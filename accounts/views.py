from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods,require_POST

# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login 
from django.contrib.auth import logout as auth_logout 


from .forms import CustomUserCreationForm, CustomAuthenticationForm

# Create your views here.

#로그인 안한 유저 대상 
@require_http_methods(['GET', 'POST'])
def signup(request):

    if request.method == 'POST' :
        form = CustomUserCreationForm(request.POST)
        if form.is_valid() : # 유효성 검사 
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:login')
    else : 
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@ require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST' :
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('game:index') #게임 실행 페이지로 이동 
    else : 
        form = CustomAuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    auth_logout(request)
    # return redirect('game:home') 게임 홈페이지로 이동 