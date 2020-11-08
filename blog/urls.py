from django.urls import path, include
from .views import PostListView, PostListViewByTag, PostDetailView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('posts/<str:tag>/', PostListViewByTag.as_view(), name='posts-by-tag'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('bio/', views.bio, name='blog-bio'),
    path('projects/', views.projects, name='projects')
]