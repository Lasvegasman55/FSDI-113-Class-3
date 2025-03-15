from django.urls import path
from .views import (
    PostListView, DraftPostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    ArchivePostListView, publish_post
)

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('drafts/', DraftPostListView.as_view(), name='drafts'),  # Updated class name
    path('archive/', ArchivePostListView.as_view(), name='archive'),  # Updated class name
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='delete'),
    path('<int:pk>/publish/', publish_post, name='publish'),
    path('new/', PostCreateView.as_view(), name='new'),
]