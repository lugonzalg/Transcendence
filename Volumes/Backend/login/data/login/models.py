from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.

class User(models.Model):

    username: str = models.CharField(max_length=16, unique=True)
    email: str = models.CharField(max_length=32, unique=True)