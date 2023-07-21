from django.contrib.auth.models import AbstractUser
from django.db import models


#Stores the details of all the registered users
class User(AbstractUser):
    bio = models.CharField(max_length=64, default="")

    def __str__(self):
        return f"username: {self.username}"


#Stores the followers of users
class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followers")
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")


#NO NEED! REMOVE IT!
class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followings")
    followings = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")


#Stores the posts of all users.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    post = models.CharField(max_length=1000, blank=False, null=False)
    likes = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"username: {self.user.username}, post: {self.post}"

    def serialize(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'post': self.post,
            'likes': self.likes,
            'timestamp': self.timestamp
        }

#INTENTION UNCLEAR
class Like(models.Model):
    user_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="user_post")
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
