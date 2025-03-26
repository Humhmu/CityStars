from django import forms
from django.contrib.auth.models import User
from CityStars_app.models import Profile, Post


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "email", "password")

        help_texts = {"username": ""}


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("profile_picture", "bio", "is_verified")

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get("profile_picture")
        if profile_picture and not hasattr(profile_picture, "file"):
            raise forms.ValidationError("Invalid file type for profile picture.")
        return profile_picture

    def clean_bio(self):
        bio = self.cleaned_data.get("bio")
        if bio and not isinstance(bio, str):
            raise forms.ValidationError("Bio must be a string.")
        return bio

    def clean_is_verified(self):
        is_verified = self.cleaned_data.get("is_verified")
        if not isinstance(is_verified, bool):
            raise forms.ValidationError("is_verified must be a boolean.")
        return is_verified


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "city", "image", "text", "rating")
