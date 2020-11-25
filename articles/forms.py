from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        label = '',
        widget=forms.TextInput(
            attrs={
                'class':"article-form",
                'placeholder':'Title 입력',
            }
        )
    )
    content = forms.CharField(
        label = '',
        widget=forms.Textarea(
            attrs={
                'class':"article-form",
                'placeholder':'내용입력'
            }
        )
    )
    rating = forms.IntegerField(
        max_value=5,
        min_value=0,
        label = '',
        widget=forms.NumberInput(
            attrs={
                'class':"article-form",
                'placeholder':' 0~5 점수로 평점을 입력해주세요',
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
        label = '',
        widget=forms.TextInput(
            attrs={
                'class':"comment-create",
                'placeholder':"댓글을 입력하세요"
            }
        )
    )
    
    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ['article', 'user',]