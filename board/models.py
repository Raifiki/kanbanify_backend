from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class board(models.Model):
    title = models.CharField(max_length=200)
    members = models.ManyToManyField(User)
    categorylist = models.CharField(max_length=200)

