from django.forms import ModelForm, BooleanField
from .models import Post, User

class PostForm(ModelForm):
    check_box = BooleanField(label='Подтвердить!')

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'postCategory']

class AuthorForm(ModelForm):

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  ]
