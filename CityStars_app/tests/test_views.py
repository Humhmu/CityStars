from django.test import Client, TestCase
from django.urls import reverse
from CityStars_app.models import *
import datetime
from django.utils import timezone
from django.utils.timezone import now
from django.core.files.uploadedfile import SimpleUploadedFile


class CityStarsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.user)
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"simple image content",
            content_type="image/jpeg",
        )
        self.city = City.objects.create(
            name="Glasgow",
            slug="Glasgow",
            image=self.image,
            desc="Glasgowdescription",
            country="Scotland",
        )
        self.city2 = City.objects.create(
            name="Edinburgh",
            slug="Edinburgh",
            image=self.image,
            desc="Edinburghdescription",
            country="Scotland",
        )
        self.post1 = Post.objects.create(
            city=self.city, user=self.profile, posted_date=now()
        )
        self.post2 = Post.objects.create(
            city=self.city,
            user=self.profile,
            posted_date=now() - datetime.timedelta(days=8),
        )

    def test_city_stars_view(self):
        response = self.client.get(reverse("CityStars_app:city_stars"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/city_stars.html")
        self.assertIn("cities", response.context)
        self.assertIn("posts", response.context)
        self.assertIn("posts_week", response.context)
        self.assertEqual(len(response.context["cities"]), 2)
        self.assertEqual(response.context["posts"]["Glasgow"], 2)

    def test_city_stars_view_no_cities(self):
        City.objects.all().delete()
        Post.objects.all().delete()
        response = self.client.get(reverse("CityStars_app:city_stars"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/city_stars.html")
        self.assertEqual(len(response.context["cities"]), 0)
        self.assertEqual(response.context["posts"], {})
        self.assertEqual(response.context["posts_week"], {})


class CityViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.user)
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"simple image content",
            content_type="image/jpeg",
        )
        self.city = City.objects.create(
            name="Glasgow",
            image=self.image,
            desc="Glasgowdescription",
            country="Scotland",
        )
        self.post1 = Post.objects.create(city=self.city, user=self.profile, likes=10)
        self.post2 = Post.objects.create(city=self.city, user=self.profile, likes=4)

    def test_city_view_with_valid_slug(self):
        response = self.client.get(
            reverse("CityStars_app:city", args=["glasgowscotland"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/city.html")
        self.assertEqual(response.context["city"].name, "Glasgow")
        self.assertEqual(len(response.context["top_posts"]), 2)

    def test_city_view_with_invalid_slug(self):
        response = self.client.get(reverse("CityStars_app:city", args=["invalid-slug"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/city.html")
        self.assertIsNone(response.context["city"])


class FriendFeedViewTest(TestCase):
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
        self.city = City.objects.create(
            name="Glasgow",
            slug="Glasgow",
            desc="Glasgowdescription",
            country="Scotland",
        )
        self.post = Post.objects.create(
            title="Friend post", city=self.city, user=self.profile2, text="Friend Post"
        )

    def test_friend_feed_view_authenticated(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get(reverse("CityStars_app:friend_feed"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/friend_feed.html")
        self.assertIn("posts", response.context)
        self.assertEqual(len(response.context["posts"]), 1)

    def test_friend_feed_view_authenticated(self):
        response = self.client.get(reverse("CityStars_app:friend_feed"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/friend_feed.html")
        self.assertEqual(len(response.context["posts"]), 0)


class CityFeedViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.user)
        self.image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"simple image content",
            content_type="image/jpeg",
        )
        self.city = City.objects.create(
            name="Glasgow",
            slug="glasgowscotland",
            image=self.image,
            desc="Glasgowdescription",
            country="Scotland",
        )
        self.post1 = Post.objects.create(
            city=self.city, user=self.profile, posted_date=now()
        )
        self.post2 = Post.objects.create(
            city=self.city,
            user=self.profile,
            posted_date=now() - datetime.timedelta(days=1),
        )

    def test_city_feed_view(self):
        response = self.client.get(reverse("CityStars_app:city_feed"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/city_feed.html")
        self.assertIn("posts", response.context)
        self.assertEqual(len(response.context["posts"]), 2)


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("CityStars_app:profile", args=["testuser"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["profile"], self.profile)

    def test_post_unauthenticated_user(self):
        response = self.client.get(reverse("CityStars_app:profile", args=["testuser"]))
        self.assertRedirects(response, reverse("CityStars_app:login"))


class DeleteProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.user, slug="testuser")

    def test_delete_profile_view_loads_correctly(self):
        response = self.client.get(
            reverse("CityStars_app:delete_profile", args=["testuser"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/delete_profile.html")


class ChatViewTest(TestCase):
    def setUp(self):
        self.client = Client()
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
        self.chat = Chat.objects.create(friendship=self.friendship)
        Message.objects.create(chat=self.chat, user=self.profile1, text="Hello!")
        Message.objects.create(chat=self.chat, user=self.profile2, text="Hi!")

    def test_chat_view_valid_access(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get(reverse("CityStars_app:chat", args=[self.profile1.slug, self.profile2.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello!")
        self.assertContains(response, "Hi!")
    
    def test_chat_view_no_friendship_redirect(self):
        self.client.login(username="testuser1", password="testpassword")
        user3 = User.objects.create_user(
            username="testuser3", password="testpassword"
        )
        Profile.objects.filter(slug="testuser3").delete()
        profile3 = Profile.objects.create(user=user3)

        response = self.client.get(reverse("CityStars_app:chat", args=[self.profile1.slug, profile3.slug]))
        self.assertEqual(response.status_code, 302) 

    def test_chat_view_unauthorized_access_redirect(self):
        self.client.login(username="testuser2", password="testpassword")

        response = self.client.get(reverse("CityStars_app:chat", args=[self.profile1.slug, self.profile2.slug]))
        self.assertEqual(response.status_code, 302)
        

class PostsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.user, slug="testuser")
        self.city = City.objects.create(
            name="Glasgow", desc="Glasgowdescription", country="Scotland"
        )
        self.post = Post.objects.create(
            city=self.city, user=self.profile, text="Test Post"
        )
        self.url = reverse(
            "CityStars_app:posts", kwargs={"profile_slug": self.profile.slug}
        )

    def test_posts_view_authenticated_user(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/posts.html")
        self.assertEqual(response.context["profile"], self.profile)
        self.assertIn(self.post, response.context["user_posts"])

    def test_posts_view_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, "/city_stars/login")


class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.user, slug="testuser")
        self.city = City.objects.create(
            name="Glasgow", desc="Glasgowdescription", country="Scotland"
        )
        self.image = SimpleUploadedFile(
            "test_image.jpg", b"simple image content", content_type="image/jpeg"
        )
        self.post = Post.objects.create(
            city=self.city, user=self.profile, text="Test Post", image = self.image,
        )

    def test_post_view_valid_postid(self):
        response = self.client.get(reverse("CityStars_app:post", args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/post.html")
        self.assertEqual(response.context["city_name"], "Glasgow")

    def test_post_view_invalid_postid(self):
        response = self.client.get(reverse("CityStars_app:post", args=[999]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/post.html")
        self.assertEqual(response.context["city_name"], "City")


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_login_valid_user(self):
        response = self.client.get(
            reverse("CityStars_app:login"),
            {"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_user(self):
        response = self.client.get(
            reverse("CityStars_app:login"),
            {"username": "wronguser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/login.html")


class UserLogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_logout(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("CityStars_app:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("CityStars_app:city_stars"))


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_valid_signup(self):
        response = self.client.get(
            reverse("CityStars_app:register"),
            {
                "username": "newuser",
                "password": "newpassword",
                "email": "newuser@test.mail",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_signup(self):
        response = self.client.post(
            reverse("CityStars_app:register"),
            {"username": "", "password": "newpassword", "email": "newuser@test.mail"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/register.html")


class AddPostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.user, slug="testuser")
        self.city = City.objects.create(
            name="Glasgow",
            slug="glasgowscotland",
            desc="Glasgowdescription",
            country="Scotland",
        )
        self.url = reverse(
            "CityStars_app:add_post", kwargs={"city_slug": self.city.slug}
        )

    def test_get_method(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/add_post.html")

    def test_post_invalid_data(self):
        self.client.login(username="testuser", password="testpassword")
        form_data = {
            "title": "",
            "text": "",
            "rating": 5,
        }
        response = self.client.post(self.url, data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "CityStars_app/add_post.html")
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Post.objects.count(), 0)


class SendFriendRequestViewTest(TestCase):
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

    def test_send_friend_request_logged_in(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get(
            reverse(
                "CityStars_app:send_friend_request",
                kwargs={"profile_slug": self.profile2.slug},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "CityStars_app:profile", kwargs={"profile_slug": self.profile2.slug}
            ),
        )
        friendship = Friendship.objects.filter(
            user_initiated=self.profile1, user_requested=self.profile2
        )
        self.assertTrue(friendship.exists())


class FriendRequestAcceptanceTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        Profile.objects.filter(slug="testuser1").delete()
        Profile.objects.filter(slug="testuser2").delete()
        self.profile1 = Profile.objects.create(user=self.user1, slug="testuser1")
        self.profile2 = Profile.objects.create(user=self.user2, slug="testuser2")
        Friendship.objects.create(
            user_initiated=self.profile1, user_requested=self.profile2, pending=True
        )

    def test_accept_friend_request_logged_in(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(
            reverse(
                "CityStars_app:accept_friend_request",
                kwargs={"profile_slug": self.profile1.slug},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "CityStars_app:profile", kwargs={"profile_slug": self.profile1.slug}
            ),
        )
        friendship = Friendship.objects.get(
            user_initiated=self.profile1, user_requested=self.profile2
        )
        self.assertFalse(friendship.pending)


class RejectFriendRequestViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        Profile.objects.filter(slug="testuser1").delete()
        Profile.objects.filter(slug="testuser2").delete()
        self.profile1 = Profile.objects.create(user=self.user1, slug="testuser1")
        self.profile2 = Profile.objects.create(user=self.user2, slug="testuser2")
        Friendship.objects.create(
            user_initiated=self.profile1, user_requested=self.profile2, pending=True
        )

    def test_reject_friend_request_logged_in(self):
        self.client.login(username="testuser2", password="testpassword")
        response = self.client.get(
            reverse(
                "CityStars_app:reject_friend_request",
                kwargs={"profile_slug": self.profile1.slug},
            )
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "CityStars_app:profile", kwargs={"profile_slug": self.profile1.slug}
            ),
        )
        with self.assertRaises(Friendship.DoesNotExist):
            Friendship.objects.get(
                user_initiated=self.profile1, user_requested=self.profile2
            )


class FriendsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        Profile.objects.filter(slug="testuser1").delete()
        Profile.objects.filter(slug="testuser2").delete()
        self.profile1 = Profile.objects.create(user=self.user1, slug="testuser1")
        self.profile2 = Profile.objects.create(user=self.user2, slug="testuser2")
        Friendship.objects.create(
            user_initiated=self.profile1, user_requested=self.profile2, pending=False
        )

    def test_friends_got_friend(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get(reverse("CityStars_app:friends", args=["testuser1"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("profile", response.context)
        self.assertIn("friends", response.context)
        friends = response.context["friends"]
        self.assertEqual(len(friends), 1)
        self.assertEqual(str(friends[0]), "Profile| testuser2")
    
    def test_friends_redirect(self):
        self.client.login(username="testuser1", password="testpassword")
        response = self.client.get(reverse("CityStars_app:friends", args=["testuser2"]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("CityStars_app:city_stars"))
