from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    title = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    
class Category(models.Model):
    title = models.CharField(max_length=200)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='categories')
    position = models.IntegerField()

