from django.contrib import admin
from .models import Post, PostImage, PostFile
# Register your models here.

class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1  # show 1 empty form

class PostFileInline(admin.TabularInline):
    model = PostFile
    extra = 1

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}  # auto-fill slug
    inlines = [PostImageInline, PostFileInline]