# Generated by Django 4.1 on 2022-09-02 03:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0011_alter_posts_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('user_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_post', to='network.posts')),
            ],
        ),
    ]