from django.contrib import admin

# Register your models here.
from .models import Photo, UserProfile


admin.site.register(UserProfile)
admin.site.register(Photo)