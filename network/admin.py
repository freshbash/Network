from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Like, Follower

class CustomUserAdmin(UserAdmin):
    pass

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Follower)
