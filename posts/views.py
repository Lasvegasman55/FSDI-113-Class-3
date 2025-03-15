from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Post
from .forms import PostForm
from django.db import models
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
      
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                models.Q(status='published') | 
                models.Q(author=self.request.user)
            )
        return queryset

class DraftPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        # Only show drafts belonging to the current user
        return Post.objects.filter(author=self.request.user, status='draft')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Drafts'
        return context

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        if obj.status == 'draft' and obj.author != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied
        return obj
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['action'] = 'Create'
    print("Loading template with context:", context)
    return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/form.html'  # Changed to match PostCreateView
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        messages.error(self.request, 'You can only edit your own posts!')
        return False
    
    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('posts:detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:list')
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        messages.error(self.request, 'You can only delete your own posts!')
        return False
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

class ArchivePostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        # Filter for archived posts belonging to the current user
        return Post.objects.filter(author=self.request.user, status='archived')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Archive'
        return context

@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # Ensure only the author can publish
    if request.user != post.author:
        messages.error(request, 'You can only publish your own posts!')
        return redirect('posts:detail', pk=pk)
    
    if request.method == 'POST':
        post.status = 'published'
        post.save()
        messages.success(request, 'Post published successfully!')
        return redirect('posts:detail', pk=pk)
    
    return redirect('posts:detail', pk=pk)