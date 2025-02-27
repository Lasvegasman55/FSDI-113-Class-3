from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('new/', views.PostCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete'),
    path('draft/', views.DraftPostListView.as_view(), name='draft'),
    # path('archieve/', views.ArchievePostListView.as_view(), name='archieve'),
  
]