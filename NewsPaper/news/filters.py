from django.forms.widgets import DateInput, TextInput, CheckboxSelectMultiple
from django_filters import FilterSet, DateFilter, CharFilter, MultipleChoiceFilter
from .models import Post


class PostFilter(FilterSet):
    datetime_create = DateFilter(
        field_name='datetime_create',
        lookup_expr='gt',
        label='Дата создания поста (позднее чем)',
        widget=DateInput(attrs={
         'placeholder': 'гггг/мм/дд',
         'class': 'form-control',
         'type': 'date'}),
        )
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Тема поста',
        widget=TextInput(attrs={'class': 'form-control'}))
    author__user__username = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора поста',
        widget=TextInput(attrs={'class': 'form-control'}))
    category__name = MultipleChoiceFilter(
        field_name='category__name',
        label='Категория',
        choices=[('games', 'games'), ('cats', 'cats'), ('cars', 'cars'), ('fun', 'fun')],
        widget=CheckboxSelectMultiple()
    )
    class Meta:
        model = Post
        fields = ['datetime_create', 'title', 'author__user__username', 'category__name']
