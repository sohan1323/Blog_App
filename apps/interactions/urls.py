from django.urls import path
from . import views

urlpatterns = [
    path('post/<slug:slug>/like/', views.toggle_like, name='toggle-like'),
    path('post/<slug:slug>/dislike/', views.toggle_dislike, name='toggle-dislike'),
]
