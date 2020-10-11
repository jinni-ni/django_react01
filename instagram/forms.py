import re

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        # form 에 지정된 필드에 관해서만 유효성 검사 함
        fields = ['message', 'photo', 'tag_set', 'is_public']

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            # message에 영어가 잇으면 영어를 없애고 저장하도록 함
            message = re.sub(r'[a-zA-Z]','',message)
        return message
