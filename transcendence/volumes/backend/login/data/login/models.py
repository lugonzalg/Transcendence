from django.db import models

# Create your models here.

class User(models.Model):

    login: str = models.CharField(max_length=16)
    email: str = models.CharField(max_length=32)
    password: str = models.CharField(max_length=64)