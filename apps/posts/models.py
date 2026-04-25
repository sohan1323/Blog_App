from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft','Draft'),
        ('published','Published'),
    ]
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(unique=True,blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True,blank=True)
    
    def save(self,*args,**kwargs):              #The save() override auto-generates a slug from the title so we don't have to type it manually
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)
        
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post-detail', kwargs={'slug': self.slug})

    @property
    def likes_count(self):
        return self.postlike_set.filter(is_like=True).count()

    @property
    def dislikes_count(self):
        return self.postlike_set.filter(is_like=False).count()

    
    
class PostImage(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='posts/images/')
    caption = models.CharField(max_length=200,blank=True)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
class PostFile(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='files'
    )
    file = models.FileField(upload_to='posts/files/')
    file_name = models.CharField(max_length=255)
    file_size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)