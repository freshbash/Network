# Generated by Django 4.2.3 on 2023-07-17 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_likes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Follower',
        ),
        migrations.RenameModel(
            old_name='Followings',
            new_name='Following',
        ),
        migrations.RenameModel(
            old_name='Likes',
            new_name='Like',
        ),
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]
