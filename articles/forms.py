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