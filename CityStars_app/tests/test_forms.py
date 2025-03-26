from django import forms
from django.test import TestCase
from django.urls import reverse
from CityStars_app.forms import PostForm, UserForm, UserProfileForm
from CityStars_app.models import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File


class UserFormTest(TestCase):
    def test_user_form_valid_data(self):
        form_data = {
            "username": "testuser",
            "email": "user@test.mail",
            "password": "testpassword",
        }

        form = UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_no_username(self):
        form_data = {
            "username": "",
            "email": "user@test.mail",
            "password": "testpassword",
        }

        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_user_form_invalid_email(self):
        form_data = {
            "username": "",
            "email": "user/test.mail",
            "password": "testpassword",
        }

        form = UserForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_user_form_password_widget(self):
        form = UserForm()
        self.assertIsInstance(form.fields["password"].widget, forms.PasswordInput)

    def test_user_form_help_texts(self):
        form = UserForm()
        self.assertEqual(form.fields["username"].help_text, "")


class UserProfileFormTest(TestCase):
    def test_user_profile_form_valid_data(self):
        user = User.objects.create(username="testuser")
        with open("static/images/DEFAULT_profile_photo.jpg", "rb") as img_file:
            image = SimpleUploadedFile(
                name="test_image.jpg",
                content=img_file.read(),
                content_type="image/jpeg",
            )
        form_data = {"bio": "Test bio", "is_verified": True}
        form_files = {"profile_picture": image}

        form = UserProfileForm(
            data=form_data, files=form_files, instance=Profile(user=user)
        )
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_user_profile_form_no_bio_pic(self):
        user = User.objects.create(username="testuser")
        form_data = {"bio": "", "is_verified": False}
        form_files = {"profile_picture": None}
        form = UserProfileForm(
            data=form_data, files=form_files, instance=Profile(user=user)
        )
        self.assertTrue(form.is_valid())

    def test_user_profile_invalid_datatypes(self):
        form_data = {"profile_picture": 999, "bio": False, "is_verified": "False"}
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())


class PostFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        Profile.objects.filter(slug="testuser").delete()
        self.profile = Profile.objects.create(user=self.user)
        with open("static/images/DEFAULT_profile_photo.jpg", "rb") as img_file:
            self.image = SimpleUploadedFile(
                name="test_image.jpg",
                content=img_file.read(),
                content_type="image/jpeg",
            )

    def test_post_form_valid_data(self):
        form_data = {
            "title": "GlasgowPostTitle",
            "text": "GlasgowPostText",
            "rating": 4,
        }

        file_data = {"image": self.image}
        form = PostForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_post_form_invalid_data(self):
        form_data = {"title": "", "text": "", "rating": None}

        file_data = {"image": None}
        form = PostForm(data=form_data, files=file_data)
        print(form.errors)

        self.assertFalse(form.is_valid())
