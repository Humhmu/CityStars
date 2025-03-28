# Generated by Django 5.1.6 on 2025-03-07 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CityStars_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_images/default_profile_pic.jpg', upload_to='profile_images'),
        ),
    ]
