from django.forms.widgets import DateInput, TextInput, CheckboxSelectMultiple
from django_filters import FilterSet, DateFilter, CharFilter, MultipleChoiceFilter
from .models import Post


class PostFilter(FilterSet):
    datetime_create = DateFilter(
        field_name='datetime_create',
        lookup_expr='gt',
        label='Дата (позднее)',
        widget=DateInput(attrs={
         'placeholder': 'гггг/мм/дд',
         'class': 'form-control',
         'type': 'date',
         'style': 'width: 8em; display: inline-block'}),
        )
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Тема поста',
        widget=TextInput(attrs={
            'class': 'form-control',
            'style': 'width: calc(100% - 8em); display: inline-block'}))
    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Автор поста',
        widget=TextInput(attrs={
            'class': 'form-control',
            'style': 'width: 10em; display: inline-block'}))
    category = MultipleChoiceFilter(
        field_name='category__name',
        label='Категория',
        choices=[('games', 'games'), ('cats', 'cats'), ('cars', 'cars'), ('fun', 'fun')],
        widget=CheckboxSelectMultiple()
    )
    class Meta:
        model = Post
        fields = ['author', 'datetime_create', 'category', 'title']
