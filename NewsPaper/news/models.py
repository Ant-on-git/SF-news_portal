from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.cache import cache

class UserSubscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through=UserSubscriber)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Types(models.TextChoices):
        article = 'статья', 'статья'
        news = 'новость', 'новость'

    type = models.CharField(max_length=7, choices=Types.choices, default=Types.article)
    datetime_create = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    category = models.ManyToManyField('Category', through='PostCategory')

    def save(self, *args, **kwargs):
        # переопределяем метод, чтобы при изменении поста он удалялся из кеша
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f"post-{self.pk}")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # после добавления поста через форму django сам перенаправляет на вохвращаемый здесь адрес
        return f'/{self.id}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:50] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.category.name


class Comment(models.Model):
    text = models.TextField()
    datetime_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(sum=Sum('rating'))['sum']
        authors_comments_rating = Comment.objects.filter(user=self.user).aggregate(sum=Sum('rating'))['sum']
        comments_rating_from_authors_posts = Comment.objects.filter(post__author=self).aggregate(sum=Sum('rating'))['sum']
        self.rating = posts_rating * 3 + authors_comments_rating + comments_rating_from_authors_posts
        self.save()

    def __str__(self):
        return self.user.username
