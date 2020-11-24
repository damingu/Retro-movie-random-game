from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label = 'Title',
        widget=forms.TextInput(
            attrs={
                'class':"my-content form-control",
            }
        )
    )
    content = forms.CharField(
        label = 'Content',
        widget=forms.Textarea(
            attrs={
                'class':"my-content form-control",
            }
        )
    )
    rating = forms.IntegerField(
        max_value=5,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                'placeholder':'0~5'
            }
        ),
        error_messages={
            'required':'평점을 입력해주세요'
        }
    )
    
    class Meta:
        model = Article
        fields = ['title','content','rating']


class CommentForm(forms.ModelForm):
    
    content = forms.CharField(
        label = 'Content',
        widget=forms.TextInput(
            attrs={
                'class':"my-content form-control",
            }
        )
    )
    
    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['article', 'user',]