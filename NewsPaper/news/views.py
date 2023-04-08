# from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Comment, Category, Author
from .filters import PostFilter
from .forms import PostForm, SubscribeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostList(ListView):
    model = Post
    template_name = 'postList.html'
    context_object_name = 'postList'
    queryset = Post.objects.order_by('-id')  # queryset встроенная переменная, по умолчанию забирает
                                             # все записи по порядку из модели. т.е. = Post.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if self.request.user.is_authenticated:
            context['username'] = user.username if user.username else user.email
            context['is_not_author'] = not user.groups.filter(name='authors').exists()
            context['links'] = ({'class': 'text-secondary', 'href': '/edit', 'text': 'редактировать'},
                                {'class': 'text-danger', 'href': '/delete', 'text': 'удалить'})
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'postDetails.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if self.request.user.is_authenticated:
            context['username'] = user.username if user.username else user.email
            context['is_not_author'] = not user.groups.filter(name='authors').exists()
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

    def get_subscribeForm(self):
        subscribeForm = SubscribeForm()
        user = self.request.user
        alredy_subscribed = Category.objects.filter(subscribers__in=[user.id])
        alredy_subscribed_list = [category.id for category in alredy_subscribed]
        subscribeForm.initial = {'name': alredy_subscribed_list}
        return subscribeForm

    def get_queryset(self):
        queryset = super().get_queryset()
        return PostFilter(self.request.GET, queryset=queryset).qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if self.request.user.is_authenticated:
            context['username'] = user.username if user.username else user.email
            context['is_not_author'] = not user.groups.filter(name='authors').exists()
            context['links'] = ({'class': 'text-secondary', 'href': '/edit', 'text': 'редактировать'},
                                {'class': 'text-danger', 'href': '/delete', 'text': 'удалить'})

        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        request_copy = self.request.GET.copy()
        clean_get = request_copy.pop('page', True) and request_copy.urlencode()
        context['clean_get_request'] = clean_get
        if not clean_get:
            context['postSearch'] = []
            context['filter.qs'] = []

        context['subscribeForm'] = self.get_subscribeForm()
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    template_name = 'postCreate.html'
    form_class = PostForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if self.request.user.is_authenticated:
            context['username'] = user.username if user.username else user.email
            context['is_not_author'] = not user.groups.filter(name='authors').exists()
        return context



class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'postCreate.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edit'] = 'изменить'
        user = self.request.user
        if self.request.user.is_authenticated:
            context['username'] = user.username if user.username else user.email
            context['is_not_author'] = not user.groups.filter(name='authors').exists()
        return context



class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    template_name = 'postDelete.html'
    queryset = Post.objects.all()
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=kwargs['object'])
        user = self.request.user
        if self.request.user.is_authenticated:
            context['username'] = user.username if user.username else user.email
            context['is_not_author'] = not user.groups.filter(name='authors').exists()
        return context



@login_required
def get_in_author_group(request):
    # добавляем в группу авторы (django.contrib.auth.models)  (там раздаем права)
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(request.user)
    # добавляем в модель авторы (news.models) (она была создана в начале хз зачем. но раз есть, то добавляем)
    authors_users = [a.user for a in Author.objects.all()]
    if request.user not in authors_users:
        Author.objects.create(user=request.user)
    redirect_from = request.META['HTTP_REFERER']
    return redirect(redirect_from)


@login_required
def subscribe(request):
    redirect_from = request.META['HTTP_REFERER']
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        user = request.user
        alredy_subscribed = Category.objects.filter(subscribers__in=[user.id])
        if form.is_valid():
            checked_categories = form.cleaned_data['name']
            for category in checked_categories:
                if category not in alredy_subscribed:
                    category.subscribers.add(user)
            for category in alredy_subscribed:
                if category not in checked_categories:
                    category.subscribers.remove(user)
    return redirect(redirect_from)