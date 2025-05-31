from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import PhotoListView,PhotoTagListView,PhotoDetailView,PhotoCreateView,PhotoUpdateView,PhotoDeleteView,SignUpView,CustomLoginView,ProfileDetailView, ProfileUpdateView,like_photo, dislike_photo

app_name = 'myapp'
urlpatterns = [
  path('', PhotoListView.as_view(), name = 'list'),
  path('tag/<slug:tag>/', PhotoTagListView.as_view(), name = 'tag'),
  path('photo/<int:pk>/', PhotoDetailView.as_view(), name = 'detail'),
  path('photo/create/', PhotoCreateView.as_view(), name = 'create'),
  path('photo/<int:pk>/update/', PhotoUpdateView.as_view(), name= 'update'),
  path('photo/<int:pk>/delete/', PhotoDeleteView.as_view(), name ='delete'),
  path('signup/', SignUpView.as_view(), name = 'signup'),
  path('login/', CustomLoginView.as_view(), name = 'login'),
  path('logout/', LogoutView.as_view(), name = 'logout'),
  path('profile/', ProfileDetailView.as_view(), name='profile'),
  path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
   path('photo/<int:pk>/like/', like_photo, name='like'),
  path('photo/<int:pk>/dislike/', dislike_photo, name='dislike'),

]