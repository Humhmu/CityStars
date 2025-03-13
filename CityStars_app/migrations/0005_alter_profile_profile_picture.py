# Generated by Django 5.1.6 on 2025-03-13 16:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CityStars_app", "0004_profile_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_picture",
            field=models.ImageField(
                blank=True,
                default="default_profile_pic.jpg",
                upload_to="profile_images",
            ),
        ),
    ]
