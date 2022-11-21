from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followed_by', blank=True)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following_to', blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_like', blank=True)
    no_of_likes = models.IntegerField(default=0)


class Comment(models.Model):
    comment = models.CharField(max_length=300, blank=True)
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    comment_at = models.DateTimeField(auto_now_add=True, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
