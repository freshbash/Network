# Generated by Django 4.1 on 2023-07-28 01:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0016_rename_datetime_post_timestamp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Following',
        ),
    ]
