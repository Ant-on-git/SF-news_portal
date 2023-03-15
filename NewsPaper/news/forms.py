from django.forms import ModelForm, fields, RadioSelect, TextInput, CheckboxSelectMultiple, NumberInput, Textarea, \
    ModelChoiceField, ModelMultipleChoiceField, Select
from .models import Post, Author, Category


class PostForm(ModelForm):
    author = ModelChoiceField(
        label='Автор',
        queryset=Author.objects.all(),
        widget=Select(attrs={'class': 'form-control', 'style': 'width: 6em; display: inline-block'})
    )
    type = fields.ChoiceField(
        label='Тип',
        choices=(('статья', 'статья'), ('пост', 'пост')),
        widget=RadioSelect()
    )
    title = fields.CharField(
        label='Название',
        widget=TextInput(attrs={'class': 'form-control'})
    )
    category = ModelMultipleChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
        widget=CheckboxSelectMultiple(attrs={'class': 'py-sm-1'})
    )
    rating = fields.IntegerField(
        label='Рейтинг',
        widget=NumberInput(attrs={'class': 'form-control', 'style': 'width: 6em; display: inline-block'})
    )
    text = fields.CharField(
        label='Содержание',
        widget=Textarea(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Post
        fields = ['author', 'type', 'title', 'category', 'rating', 'text']