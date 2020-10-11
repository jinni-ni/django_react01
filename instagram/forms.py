from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        # form 에 지정된 필드에 관해서만 유효성 검사 함
        fields = ['message', 'photo', 'tag_set', 'is_public']
