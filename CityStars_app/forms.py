from django import forms
from django.contrib.auth.models import User
from CityStars_app.models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

        help_texts = {'username':''}

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_picture', 'bio', 'is_verified')