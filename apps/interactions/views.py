from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.posts.models import Post
from .models import PostLike

# Create your views here.
@login_required
def toggle_like(request,slug):
    post = get_object_or_404(Post,slug=slug)
    like_obj, created = PostLike.objects.get_or_create(
        user = request.user,
        post=post,
        defaults={'is_like':True}
    )
    if not created:
        if like_obj.is_like:
            like_obj.delete()
        else:
            like_obj.is_like = True
            like_obj.save()
    return redirect('post-detail',slug=slug)


@login_required
def toggle_dislike(request,slug):
    post = get_object_or_404(Post, slug=slug)
    like_obj, created = PostLike.objects.get_or_create(
        user=request.user,
        post=post,
        defaults={'is_like': False}
    )
    if not created:
        if not like_obj.is_like:
            like_obj.delete()         # un-dislike
        else:
            like_obj.is_like = False  # was like → now dislike
            like_obj.save()
    return redirect('post-detail', slug=slug)