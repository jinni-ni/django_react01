
from django.db import models
# 권장하지 않음 : User 모델이 변경 될 수 있기 때문
# from django.contrib.auth.models import User

# 권장 : settings의 auth_user_model만 수정하면 되기 때문
# 초반에 설쟁 하는게 중요
from django.conf import settings

# Create your models here.
from django.urls import reverse

# validator 는 직접 구현하면 migration 시 오류가 날 수 있기 때문에
# 기본으로 지원되는 validator 사용 권장
from django.core.validators import MinLengthValidator



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(
        validators=[MinLengthValidator(10)]
    )
    # 삭제 해야 된다면
    # ImageField를 Custom 해서 파일 삭제
    # 배치를 통해서 삭제 하는 방법

    # uplaod_to 는 함수를 지정 할 수 있음 -> 파일 경로를 지정
    photo = models.ImageField(blank=True, upload_to='instagram/post/%Y/%m/%d')
    tag_set = models.ManyToManyField('Tag', blank=True)
    is_public = models.BooleanField(default=False, verbose_name='공개여부')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        #return f"object ({self.id})"
        return self.message

    def get_absolute_url(self):
        return reverse('instagram:post_detail', args=[self.pk])

    class Meta:
        ordering = ['-id']
    # 인자 없는 함수만 가능
    # def message_length(self):
    #     return len(self.message)
    #
    # message_length.short_description = '메세지 글자수'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             limit_choices_to={'is_public': True})
    message = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)
    # post_set
    def __str__(self):
        return self.name
