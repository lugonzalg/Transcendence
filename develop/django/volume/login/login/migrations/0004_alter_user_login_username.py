# Generated by Django 5.0.1 on 2024-03-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_alter_user_login_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_login',
            name='username',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
