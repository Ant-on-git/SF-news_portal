from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, get_in_author_group


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='detail_post'),
    path('search', PostSearch.as_view(), name='search_post'),
    path('add', PostCreate.as_view(), name='create_post'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='update_post'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete_post'),
    path('get_in_author_group', get_in_author_group, name='get_in_author_group'),
]