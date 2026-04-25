from django.db import models
from django.contrib.auth.models import User
from apps.posts.models import Post

# Create your models here.
class PostLike(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    is_like = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','post')       # One vote per user per post