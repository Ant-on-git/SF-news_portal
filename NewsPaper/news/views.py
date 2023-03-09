# from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import Post, Comment, Category


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