# Create your models here.
from django.db import models


from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    publication_date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='posts')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
