# Generated by Django 5.1 on 2024-08-22 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_post_likes_remove_post_reposts_post_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='keywords',
            field=models.TextField(blank=True, null=True),
        ),
    ]
