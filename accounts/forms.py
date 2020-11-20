from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm) : 

        model = get_user_model()
        fields = UserCreationForm.Meta.fields
    
    # game 'youtube' 빼고...? =>
    # article+장바구니 // accounts 기능구현!