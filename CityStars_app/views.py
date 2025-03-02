from django.http import HttpResponse
from django.shortcuts import render


def city_stars(request):
    return render(request, 'CityStars_app/city_stars.html')


def city(request, city_slug):
    return render(request, 'CityStars_app/city.html')


def add_post(request, city_slug):
    return render(request, 'CityStars_app/add_post.html')


def friend_feed(request):
    return render(request, 'CityStars_app/friend_feed.html')


def city_feed(request):
    return render(request, 'CityStars_app/city_feed.html')


def profile(request, profile_username):
    return render(request, 'CityStars_app/profile.html')


def delete_profile(request, profile_username):
    return render(request, 'CityStars_app/delete_profile.html')


def friends(request, profile_username):
    return render(request, 'CityStars_app/friends.html')


def chat(request, profile_username, friend_username):
    return render(request, 'CityStars_app/chat.html')


def posts(request, profile_username):
    return render(request, 'CityStars_app/posts.html')


def city_post(request, city_slug, post_id):
    return render(request, 'CityStars_app/city_post.html')


def user_post(request, profile_username, post_id):
    return render(request, 'CityStars_app/user_post.html')


def delete_post(request, post_id):
    return render(request, 'CityStars_app/delete_post.html')


def login(request):
    return render(request, 'CityStars_app/login.html')


def signup(request):
    return render(request, 'CityStars_app/register.html')
