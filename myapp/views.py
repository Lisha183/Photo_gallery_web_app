from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Photo, UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, PhotoForm

class PhotoListView(ListView):
    model = Photo
    template_name = 'list.html'
    context_object_name = 'photos'

class PhotoTagListView(PhotoListView):
    template_name = 'taglist.html'

    def get_tag(self):
        return self.kwargs.get('tag')
    
    def get_queryset(self):
        return self.model.objects.filter(tags__slug=self.get_tag())
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.get_tag()
        return context

class PhotoDetailView(DetailView):
    model = Photo
    template_name = 'detail.html'
    context_object_name = 'photo'

class PhotoCreateView (LoginRequiredMixin, CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'create.html'
    success_url = reverse_lazy('photo:list')

    def form_valid (self, form):
        form.instance.submitter = self.request.user
        return super ().form_valid(form)

class UserIsSubmitter(UserPassesTestMixin):
    def get_photo(self):
        return get_object_or_404(Photo, pk =self.kwargs.get('pk'))
    
    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user == self.get_photo().submitter
        else:
            raise PermissionDenied("Sorry you are not allowed here")
        
class PhotoUpdateView(UserIsSubmitter, UpdateView):
    template_name = 'update.html'
    model = Photo
    fields = ['title', 'description', 'tags', 'image']
    success_url = reverse_lazy('photo:list')

class PhotoDeleteView(UserIsSubmitter, DeleteView):
    template_name = 'delete.html'
    model = Photo
    success_url = reverse_lazy('photo:list')

class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = SignUpForm  
    success_url = reverse_lazy('photo:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        if user is not None:
            login(self.request, user)
        return response

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.userprofile

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['bio', 'profile_pic']
    template_name = 'update.html'
    success_url = reverse_lazy('photo:profile')

    def get_object(self):
        return self.request.user.userprofile


@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.disliked_by.all():
        photo.disliked_by.remove(request.user)
    photo.liked_by.add(request.user)
    return redirect('photo:detail', pk=pk)  

@login_required
def dislike_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.liked_by.all():
        photo.liked_by.remove(request.user)
    photo.disliked_by.add(request.user)
    return redirect('photo:detail', pk=pk) 