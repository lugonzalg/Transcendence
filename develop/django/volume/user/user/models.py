from django.db import models

class user_login(models.Model):

    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=32, unique=True)
    password = models.CharField(max_length=100)
    last_log = models.DateTimeField(auto_now=True)
    mode = models.SmallIntegerField(default=0)
    avatar = models.CharField(max_length=120, default='/var/www/avatar/default.png')

    class Meta:
        db_table = 'user_login'
        managed = False

# Create your models here.
class Friends(models.Model):

    user = models.ForeignKey(user_login, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(user_login, related_name='users', on_delete=models.CASCADE)
    status = models.SmallIntegerField(default=0)
    challenge = models.SmallIntegerField(default=0)

    class Meta:
        unique_together = ('user', 'friend')

class MatchHistory(models.Model):

    p1 = models.ForeignKey(user_login, related_name='p1_matches', on_delete=models.CASCADE)
    p1_score = models.SmallIntegerField(user_login)
    p2 = models.ForeignKey(user_login, related_name='p2_matches', on_delete=models.CASCADE)
    p2_score = models.SmallIntegerField(user_login)
    date = models.DateField()

    class Meta:
        db_table = 'user_matches'