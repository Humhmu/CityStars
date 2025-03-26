from django.test import TestCase
from django.contrib.auth.models import User
from CityStars_app.models import Profile


class UserProfileSignalsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_create_user_profile_signal(self):
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)

    def test_save_user_profile_signal(self):
        self.user.username = "updateduser"
        self.user.save()
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)

    def test_save_user_profile_signal_no_profile(self):
        Profile.objects.filter(user=self.user).delete()
        self.user.username = "updateduser"
        self.user.save()
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)
