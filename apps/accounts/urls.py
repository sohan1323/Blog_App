from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('register/',views.register_view,name='register'),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/<int:pk>/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('profile/<int:pk>/delete/', views.ProfileDeleteView.as_view(), name='profile-delete'),
]
