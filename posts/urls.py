
from django.urls import path
from .views import PostListCreateView, delete_all_posts

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('delete_all_posts', delete_all_posts)
]







