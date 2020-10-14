from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View, ArchiveIndexView, YearArchiveView, CreateView, UpdateView, \
    DeleteView
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm


class PostDeleveView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('instagram:post_list')

post_delete = PostDeleveView.as_view()
#
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request,'포스팅 삭제했습니다.')
#         return redirect('instagram:post_list')
#     return render(request, 'instagram/post_confirm_delete.html',{
#         'post':post,
#     })

# @login_required -> LoginRequiredMixin
class PostUpdateView(LoginRequiredMixin,UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        messages.success(self.request, '포스팅을 수정 했습니다.')
        return super().form_valid(form)

post_edit = PostUpdateView.as_view()

#
# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     if post.author != request.user:
#         messages.error(request, '작성자만 수정할 수 있습니다.')
#         # post detail 로 이동, get_absolute_url
#         return redirect(post)
#
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             # request.user 를 사용하려면 필수로  login 되어 있어야 함 -> @login_required 사용
#             post.author = request.user
#             post.save()
#             messages.success(request, '포스팅 수정 완료')
#             # post = form.save(commit=False)
#             # post.save()
#             return redirect(post)
#     else:
#         form = PostForm(instance=post)
#
#     return render(request, 'instagram/post_new.html', {
#         'form': form,
#         'post': post,
#     })


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'instagram/post_new.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        messages.success(self.request, '포스팅을 저장했습니다.')
        return super().form_valid(form)

post_new = PostCreateView.as_view()

# # @csrf_exempt
# @login_required
# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             # post = form.save(commit=False)
#             # post.save()
#             messages.success(request,'포스팅 저장 완료')
#             return redirect(post)
#     else:
#         form = PostForm()
#
#     return render(request, 'instagram/post_new.html',{
#         'form' : form,
#     })

# Create your views here.
# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains=q)
#
#     # messages.info(request,'messages 테스트')
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
