from django.db import models
from django.conf import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blogpost_like', blank=True)

    def number_of_likes(self):
        return self.likes.count()
