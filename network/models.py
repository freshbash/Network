from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.CharField(max_length=64, default="")

    def __str__(self):
        return f"username: {self.username}"

class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followers")
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

class Followings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followings")
    followings = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    post = models.CharField(max_length=1000, blank=False, null=False)
    likes = models.IntegerField(default=0)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"username: {self.user.username}, post: {self.post}"

    def serialize(self):
        return {
            'user': self.user,
            'post': self.post,
            'likes': self.likes,
            'datetime': self.datetime
        }

class Likes(models.Model):
    user_post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="user_post")
    like = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
