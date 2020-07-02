from django.urls import path
from .views import (
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    CountryListView,
    SearchPostView,
)
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('search/', SearchPostView.as_view(), name='search-post'),
    path('country/<int:id>/', CountryListView.as_view(), name='blog-country'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('about/', views.about, name='blog-about'),
    path('like/<int:pk>/', views.PostLikeView, name='like-post'),
]