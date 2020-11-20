from django.urls import path, include
from . import views 


app_name = 'accounts'
urlpatterns = [
    # CR
    path('signup/', views.signup, name='signup'),
    # CR
    path('login/', views.login, name='login'),
    # D
    path('logout/', views.logout, name='logout'),
]