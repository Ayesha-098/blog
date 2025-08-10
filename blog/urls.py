from django.urls import path
from .views import (
    SignupView,
    PublishedPostsView,
    MyPostsView,
    CreatePostView,
    UpdatePostView,
    DeletePostView,
    PostDetailView,
)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', PublishedPostsView.as_view(), name='published_posts'),
    path('my-posts/', MyPostsView.as_view(), name='my_posts'),
    path('posts/create/', CreatePostView.as_view(), name='create_post'),
    path('posts/update/<int:pk>/', UpdatePostView.as_view(), name='post_update'),
    path('posts/delete/<int:pk>/', DeletePostView.as_view(), name='post_delete'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
]
