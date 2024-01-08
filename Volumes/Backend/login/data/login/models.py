from django.db import models

# Create your models here.

class User(models.Model):

    login: str = models.CharField(max_length=16, unique=True)
    email: str = models.CharField(max_length=32, unique=True)
    password: str = models.CharField(max_length=64, unique=True)