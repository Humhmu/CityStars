# Generated by Django 5.1.6 on 2025-03-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CityStars_app', '0006_remove_post_likes_post_liked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, default='Hey! Im new here!', max_length=1000),
        ),
    ]
