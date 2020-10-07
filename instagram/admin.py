from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Comment
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['pk', 'photo_tag', 'message', 'message_length', 'is_public','create_at', 'update_at']
    list_display_links = ['pk', 'message']
    list_filter = ['create_at', 'is_public']
    search_fields = ['message']

    # 사진이 없을 때 post.phto.url 호출 시 validate error 발생
    # 반드시 photo_tag 같은 것이 필요함
    def photo_tag(self, post):
        if post.photo:
            return mark_safe(f'<img src="{post.photo.url}" style="width:70px"/>')
        return None

    def message_length(self, post):
        return f"{len(post.message)} 글자"

    message_length.short_description = '메세지 글자수'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
