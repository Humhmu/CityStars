from django.forms import ValidationError
from django.test import TestCase
from CityStars_app.models import *


class CityModelTest(TestCase):
    def setUp(self):
        self.city = City.objects.create(name="Glasgow", country="Scotland")

    def test_city_creation(self):
        self.assertEqual(self.city.name, "Glasgow")
        self.assertEqual(self.city.country, "Scotland")
        self.assertEqual(self.city.avg_rating, 1)

    def test_slug_generation(self):
        self.assertEqual(self.city.slug, "glasgowscotland")

    def test_rating_validation(self):
        self.city.avg_rating = 6
        with self.assertRaises(ValidationError):
            self.city.full_clean()

    def test_to_string(self):
        self.assertEqual(str(self.city), "City| Glasgow")


class ProfileModelTest(TestCase):
    def setUp(self):
        self.userprofile = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.userprofile)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(
            self.profile.profile_picture, "profile_images/DEFAULT_profile_photo.jpg"
        )
        self.assertEqual(self.profile.bio, "No biography written")
        self.assertFalse(self.profile.is_verified)
        self.assertEqual(self.profile.slug, "testuser")

    def tearDown(self):
        self.profile.delete()


class PostModelTest(TestCase):
    def setUp(self):
        self.userpost = User.objects.create_user(
            username="testpostuser", password="testpassword"
        )
        Profile.objects.filter(slug="testpostuser").delete()
        self.profile = Profile.objects.create(user=self.userpost)
        self.city = City.objects.create(name="Glasgow", country="Scotland")
        self.post = Post.objects.create(
            city=self.city,
            user=self.profile,
            text="I like Glasgow",
            title="GlasgowReview",
            rating=3,
        )

    def test_post_creation(self):
        self.assertEqual(self.post.text, "I like Glasgow")
        self.assertEqual(self.post.title, "GlasgowReview")
        self.assertEqual(self.post.rating, 3)
        self.assertEqual(self.post.likes, 0)

    def test_post_no_title(self):
        self.postNoTitle = Post.objects.create(
            city=self.city, user=self.profile, text="I like Glasgow", rating=3
        )
        self.assertEqual(self.postNoTitle.title, "")

    def test_post_rating_constraints(self):
        self.post.rating = 6
        with self.assertRaises(ValidationError):
            self.city.full_clean()

    def test_post_to_string(self):
        self.assertEqual(str(self.post), "Post| City| Glasgow & Profile| testpostuser")


class FriendshipModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        Profile.objects.filter(slug="testuser1").delete()
        Profile.objects.filter(slug="testuser2").delete()
        self.profile1 = Profile.objects.create(user=self.user1)
        self.profile2 = Profile.objects.create(user=self.user2)
        self.friendship = Friendship.objects.create(
            user_initiated=self.profile1, user_requested=self.profile2
        )

    def test_friendship_creation(self):
        self.assertEqual(self.friendship.user_initiated, self.profile1)
        self.assertEqual(self.friendship.user_requested, self.profile2)
        self.assertTrue(self.friendship.pending)

    def test_friendship_uniqueness(self):
        with self.assertRaises(Exception):
            Friendship.objects.create(
                user_initiated=self.profile1, user_requested=self.profile2
            )


class ChatModelTest(TestCase):
    def setUp(self):
        self.userchat1 = User.objects.create_user(
            username="testchatuser1", password="testpassword"
        )
        self.userchat2 = User.objects.create_user(
            username="testchatuser2", password="testpassword"
        )
        Profile.objects.filter(slug="testchatuser1").delete()
        Profile.objects.filter(slug="testchatuser2").delete()
        self.profile1 = Profile.objects.create(user=self.userchat1)
        self.profile2 = Profile.objects.create(user=self.userchat2)
        self.friendship = Friendship.objects.create(
            user_initiated=self.profile1, user_requested=self.profile2
        )
        self.chat = Chat.objects.create(friendship=self.friendship)

    def test_chat_creation(self):
        self.assertEqual(str(self.chat), f"Chat| {self.friendship}")


class MessageModelTets(TestCase):
    def setUp(self):
        self.usermessage1 = User.objects.create_user(
            username="testmessageuser1", password="testpassword"
        )
        self.usermessage2 = User.objects.create_user(
            username="testmessageuser2", password="testpassword"
        )
        Profile.objects.filter(slug="testmessageuser1").delete()
        Profile.objects.filter(slug="testmessageuser2").delete()
        self.profile1 = Profile.objects.create(user=self.usermessage1)
        self.profile2 = Profile.objects.create(user=self.usermessage2)
        self.friendship = Friendship.objects.create(
            user_initiated=self.profile1, user_requested=self.profile2
        )
        self.chat = Chat.objects.create(friendship=self.friendship)
        self.message = Message.objects.create(
            chat=self.chat, user=self.profile1, text="Hello profile2"
        )

    def test_message_creation(self):
        self.assertEqual(self.message.text, "Hello profile2")
        self.assertEqual(self.message.user, self.profile1)
        self.assertEqual(self.message.chat, self.chat)

    def test_message_to_string(self):
        self.assertEqual(str(self.message), "Message| Profile| testmessageuser1")
