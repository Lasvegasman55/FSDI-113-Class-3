from django.views.generic import UpdateView, DeleteView
from .models import Post 
from django.urls import reverse_lazy

class PostUpdateView(UpdateView):
    template_name = 'posts/edit.html'
    model = Post
    fields = [
        "title", "subtitle", "body",
        "author",
    ]

class PostDeleteView(DeleteView):  
    template_name = "posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")