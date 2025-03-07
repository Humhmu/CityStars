# Generated by Django 5.1.6 on 2025-03-07 09:10

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pending', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('country', models.CharField(max_length=30)),
                ('avg_rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('image', models.ImageField(blank=True, upload_to='city_images')),
                ('desc', models.CharField(default='', max_length=300)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'ordering': ['country'],
                'constraints': [models.UniqueConstraint(fields=('name', 'country'), name='name&countryUnique')],
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friendship', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='CityStars_app.friendship')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, upload_to='profile_images')),
                ('bio', models.CharField(max_length=1000)),
                ('is_verified', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_date', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, upload_to='post_images')),
                ('text', models.CharField(max_length=500)),
                ('title', models.CharField(default='', max_length=15)),
                ('rating', models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('likes', models.IntegerField(default=0)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CityStars_app.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CityStars_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=200)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CityStars_app.chat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CityStars_app.profile')),
            ],
        ),
        migrations.AddField(
            model_name='friendship',
            name='user_initiated',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_initiated', to='CityStars_app.profile'),
        ),
        migrations.AddField(
            model_name='friendship',
            name='user_requested',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_requested', to='CityStars_app.profile'),
        ),
        migrations.AddConstraint(
            model_name='friendship',
            constraint=models.UniqueConstraint(fields=('user_initiated', 'user_requested'), name='freindshipUnique'),
        ),
    ]
