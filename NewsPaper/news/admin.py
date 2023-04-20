from django.contrib import admin
from .models import Category, Post, Comment, Author, PostCategory, UserSubscriber
from django.db.models.fields.reverse_related import ManyToManyRel

# Register your models here.
admin.site.register(Comment)
admin.site.register(Author)


# добавляем кастомное действие для модели посты (обнулить рейтинг выбранных постов)
def nullify_post_rating(modeladmin, request, queryset):  # request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(rating=0)

nullify_post_rating.short_description = 'обнулить рейтинг'  # описание для более понятного представления в админ панеле задаётся, как будто это объект


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = (PostCategoryInline,)

    list_display = ('title', 'type', 'rating', 'author', 'datetime_create', 'preview')
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in Product._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения
    # sf предлагал сделать через оператор, но в модели Post есть поле m2m, которое так вывсти нельзя.

    list_filter = ['type', 'author', 'datetime_create', 'category']
    search_fields = ['title']

    actions = [nullify_post_rating]

admin.site.register(Post, PostAdmin)


class CategorySubscriberInline(admin.TabularInline):
    model = UserSubscriber
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = (CategorySubscriberInline,)


admin.site.register(Category, CategoryAdmin)