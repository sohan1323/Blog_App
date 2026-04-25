from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.views.generic import DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Profile

# Create your views here.
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        fields = ['username','email','password1','password2']
        

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request,'accounts/register.html',{'form':form})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    
    def get_object(self, queryset=None):
        if 'pk' in self.kwargs:
            return super().get_object(queryset)
        return self.request.user.profile

class ProfileDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Profile
    template_name = 'accounts/profile_confirm_delete.html'
    success_url = reverse_lazy('home')
    
    def test_func(self):
        profile = self.get_object()
        user = self.request.user
        return user == profile.user or user.is_superuser

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    fields = ['profile_image', 'name', 'bio']
    template_name = 'accounts/profile_form.html'
    
    def get_success_url(self):
        return reverse_lazy('profile-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user