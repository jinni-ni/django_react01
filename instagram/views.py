from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, View, ArchiveIndexView, YearArchiveView
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.
# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains=q)
#     return render(request, 'instagram/post_list.html',{
#         'post_list' : qs,
#         'q' : q,
#     })

# post_list = login_required(ListView.as_view(model=Post, paginate_by=10))
#
# @method_decorator(login_required, name='dispatch' )
# class PostListView(ListView):
#     model = Post
#     paginate_by = 10


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10
post_list = PostListView.as_view()
# def post_detail(request: HttpRequest, pk: int) -> HttpResponse:
#     # try:
#     #     post = Post.objects.get(pk=pk) #DoesNotExist
#     # except:
#     #     raise Http404
#
#     post = get_object_or_404(Post,pk=pk)
#     return render(request, 'instagram/post_detail.html',{
#         'post' : post,
#     })

# post_detail = DetailView.as_view(
#     model=Post,
#     # is_public 은 boolean 값
#     queryset=Post.objects.filter(is_public=True)
# )

class PostDetailView(DetailView):
    model = Post

    # 로그인 시 is_public false, true
    # 미로그인은 is_public true
    def get_queryset(self):
        # 재정의 시 super 호출
        # 부모 view가 만든 query set 먼저 호출
        qs = super().get_queryset()
        # 로그인 되어 있으면 is_public True 인 것
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=True)
        return qs


post_detail = PostDetailView.as_view()

# def archives_year(request, year):
#     return HttpResponse(f"{year}년 archives")

post_archive = ArchiveIndexView.as_view(model=Post, date_field = 'create_at', paginate_by=10)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='create_at', make_object_list=True  )
