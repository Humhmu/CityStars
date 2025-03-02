from django.http import HttpResponse
from django.shortcuts import render


def city_stars(request):
    return render(request, "CityStars_app/base.html")


def city(request, city_slug):
    return HttpResponse("City Page")


def add_post(request, city_slug):
    return HttpResponse("Add Post Page")


def friend_feed(request):
    return HttpResponse("Friend Feed Page")


def city_feed(request):
    return HttpResponse("City Feed Page")


def profile(request, profile_username):
    return HttpResponse("Profile Page")


def delete_profile(request, profile_username):
    return HttpResponse("Delete Profile Page")


def friends(request, profile_username):
    return HttpResponse("Friends Page")


def chat(request, profile_username, friend_username):
    return HttpResponse("Chat Page")


def posts(request, profile_username):
    return HttpResponse("Posts Page")


def city_post(request, city_slug, post_id):
    return HttpResponse("Post Page")


def user_post(request, user_id, post_id):
    return HttpResponse("Post Page")


def delete_post(request, post_id):
    return HttpResponse("Delete post page")


def login(request):
    return HttpResponse("Login Page")


def signup(request):
    return HttpResponse("Signup Page")
