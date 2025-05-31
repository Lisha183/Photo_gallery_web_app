from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


User = get_user_model()

class Photo (models.Model):
    title = models.CharField(max_length = 45)
    description = models.CharField(max_length = 250)
    created = models.DateTimeField(auto_now_add= True)
    image= CloudinaryField('image', null=True)
    submitter = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    liked_by = models.ManyToManyField(User, related_name='liked_photos', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='disliked_photos', blank=True)

    def like_count(self):
        return self.liked_by.count()

    def dislike_count(self):
        return self.disliked_by.count()

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = CloudinaryField('image', null = True)

    def __str__(self):
        return f"{self.user.username}'s profile"
