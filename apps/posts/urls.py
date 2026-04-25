from django.urls import path
from . import views

urlpatterns = [
    path('',views.PostListView.as_view(),name='home'),
    path('posts/create/',views.PostCreateView.as_view(),name='post-create'),
    path('posts/<slug:slug>/',views.PostDetailView.as_view(),name='post-detail'),
    path('posts/<slug:slug>/edit/',views.PostUpdateView.as_view(),name='post-update'),
    path('posts/<slug:slug>/delete/',views.PostDeleteView.as_view(),name='post-delete'),
    
]
