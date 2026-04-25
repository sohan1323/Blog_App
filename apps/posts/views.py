from django.shortcuts import render
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import (LoginRequiredMixin,UserPassesTestMixin)
from django.urls import reverse_lazy
from .models import Post
# Create your views here.

class PostOwnerOrSuperuserMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        user = self.request.user
        return user == post.author or user.is_superuser

class PostListView(ListView):
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(
            status='published'
        ).select_related('author', 'author__profile')\
        .prefetch_related('images')\
        .order_by('-created_at')
        
        
class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content','status']
    template_name = 'posts/post_form.html'
    
    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):       #LoginRequiredMixin redirects non-logged-in users to the login page. UserPassesTestMixin blocks unauthorized users.
    model = Post
    fields = ['title','content','status']
    template_name = 'posts/post_form.html'
    
    def test_func(self):            # Permission check
        post = self.get_object()
        return self.request.user == post.author
    
    
class PostDeleteView(LoginRequiredMixin,PostOwnerOrSuperuserMixin,DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('home')
