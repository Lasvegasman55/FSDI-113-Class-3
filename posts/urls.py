from django.urls import path
from .views import DraftListView, ArchiveListView
from . import views
app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('new/', views.PostCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('draft/', views.DraftPostListView.as_view(), name='draft'),
    path('drafts/', views.DraftListView.as_view(), name='draft'),
    path('archive/', views.ArchievePostListView.as_view(), name='archieve'),
    path('archive/', views.ArchiveListView.as_view(), name='archieve'),
]