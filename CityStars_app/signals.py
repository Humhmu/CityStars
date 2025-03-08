from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from CityStars_app.models import Profile

# creates a user profile for the user and connects profile to user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) 

# saves profile when its been updated, if user doesnt have a profile creates one
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
