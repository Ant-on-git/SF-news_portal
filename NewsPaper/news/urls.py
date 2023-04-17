from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, get_in_author_group, subscribe
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60*1)(PostList.as_view())),  # кешируем страницу на 60 секунд
    path('<int:pk>', PostDetail.as_view(), name='detail_post'),
    path('search', PostSearch.as_view(), name='search_post'),
    path('add', PostCreate.as_view(), name='create_post'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='update_post'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete_post'),
    path('get_in_author_group', get_in_author_group, name='get_in_author_group'),
    path('subscribe', subscribe, name='subscribe'),
]