from django.http import HttpResponse
from django.shortcuts import render


def city_stars(request):
    return render(request, "CityStars_app/base.html")


def city(request, city_slug):
    return HttpResponse(f"City Page for {city_slug}")


def add_post(request, city_slug):
    return HttpResponse(f"page to add post to {city_slug}")


def friend_feed(request):
    return HttpResponse("Friend Feed Page")


def city_feed(request):
    return HttpResponse("City Feed Page")


def profile(request, profile_username):
    return HttpResponse(f"{profile_username}'s profile page")


def delete_profile(request, profile_username):
    return HttpResponse(f"Page to delete {profile_username}'s profile")


def friends(request, profile_username):
    return HttpResponse(f"{profile_username}'s friends page")


def chat(request, profile_username, friend_username):
    return HttpResponse(f"{profile_username}'s chat with {friend_username}")


def posts(request, profile_username):
    return HttpResponse(f"Posts page for {profile_username}")


def city_post(request, city_slug, post_id):
    return HttpResponse(f"Post {post_id} in {city_slug}")


def user_post(request, profile_username, post_id):
    return HttpResponse(f"Post {post_id} from {profile_username}")


def delete_post(request, post_id):
    return HttpResponse(f"Delete post {post_id}")


def login(request):
    return HttpResponse("Login Page")


def signup(request):
    return HttpResponse("Signup Page")
