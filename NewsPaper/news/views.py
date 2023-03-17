# from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment, Category
from .filters import PostFilter
from .forms import PostForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        request_copy = self.request.GET.copy()
        clean_get = request_copy.pop('page', True) and request_copy.urlencode()
        context['clean_get_request'] = clean_get
        if not clean_get:
            context['postSearch'] = []
            context['filter.qs'] = []
        return context


class PostCreate(CreateView):
    template_name = 'postCreate.html'
    form_class = PostForm


class PostUpdate(UpdateView):
    template_name = 'postCreate.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = 'изменить'

        return context



class PostDelete(DeleteView):
    template_name = 'postDelete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=kwargs['object'])
        return context