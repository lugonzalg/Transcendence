from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.

#esta clase se usa para llamar a la tabla de la bbdd llamada user_login
class user_login(models.Model):

    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=100)
    last_log = models.DateTimeField(auto_now=True)
    mode = models.SmallIntegerField(default=0)
    avatar = models.CharField(max_length=120, default='/avatar/default/default.png')

    class Meta:
        db_table = 'user_login'