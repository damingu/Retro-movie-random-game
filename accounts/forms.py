from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(UserCreationForm):
    # forms.py를 내 멋대로 정의
    username = forms.CharField(
        label = '',
        widget = forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'username',
        }),
        error_messages = {
            'required': '올바른 username을 입력하세요.'
        }
    )

    password1 = forms.CharField( # models.py의 type
        label = '',
        widget = forms.PasswordInput(attrs={ # Input type 
            'class': 'form-control',
            'placeholder': 'password',
        }),
        error_messages= {
            'required': '올바른 password를 입력하세요.'
        }
    )
    
    password2 = forms.CharField(
        label = '',
        widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password 확인'
        }),
        error_messages= {
            'required': 'password를 확인해 주세요.'
        }
    )

    class Meta(UserCreationForm) : 

        model = get_user_model()
        fields = UserCreationForm.Meta.fields 
        