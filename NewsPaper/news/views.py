# from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import Post, Comment, Category
from .filters import PostFilter


class PostList(ListView):
    model = Post
    template_name = 'postList.html'
    context_object_name = 'postList'
    queryset = Post.objects.order_by('-id')  # queryset встроенная переменная, по умолчанию забирает
                                             # все записи по порядку из модели. т.е. = Post.objects.all()


class PostDetail(DetailView):
    model = Post
    template_name = 'postDetails.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        # сначала вызываем базовую реалзацю
        context = super().get_context_data(**kwargs)
        # добавляем комменты к статье
        context['comments'] = Comment.objects.filter(post=kwargs['object'])
        # добавляем категории
        context['categories'] = Category.objects.all()
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'postSearch.html'
    context_object_name = 'postSearch'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self):
        context = super().get_context_data()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        request_copy = self.request.GET.copy()
        clean_get = request_copy.pop('page', True) and request_copy.urlencode()
        context['clean_get_request'] = clean_get
        if not clean_get:
            context['postSearch'] = []
            context['filter.qs'] = []
        return context