from django import forms
from .models import Movie,MovieComment

class CommentForm(forms.ModelForm):
    
    content = forms.CharField(
        label = '',
        widget=forms.TextInput(
            attrs={
                'class':"my-content form-control2 ",
                
            }
        )
    )
    class Meta:
        model = MovieComment
        # fields = '__all__'
        exclude = ['movie', 'user',]