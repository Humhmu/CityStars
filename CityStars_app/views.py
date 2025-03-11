from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from CityStars_app.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from CityStars_app.models import *
import datetime


def city_stars(request):
    context_dict = {}
    context_dict["cities"] = City.objects.order_by("name")

    context_dict["posts"] = {}
    for city in context_dict["cities"]:
        context_dict["posts"].setdefault(city.name, len(Post.objects.filter(city=city)))

    context_dict["posts_week"] = {}
    for city in context_dict["cities"]:
        context_dict["posts_week"].setdefault(
            city.name,
            len(
                Post.objects.filter(
                    city=city,
                    posted_date=datetime.datetime.now() - datetime.timedelta(weeks=1),
                )
            ),
        )

    return render(request, "CityStars_app/city_stars.html", context_dict)


def city(request, city_slug):
    context_dict = {}
    try:
        city = City.objects.get(slug=city_slug)
        context_dict["city_name"] = city.name
        context_dict["city_desc"] = city.desc
        context_dict["city_country"] = city.country

        context_dict["top_posts"] = Post.objects.filter(city = city).order_by('-likes')[:3]
    except City.DoesNotExist:
        context_dict["city_name"] = None
        context_dict["city_desc"] = None
        context_dict["city_country"] = None
        context_dict["top_posts"] = []

    return render(request, 'CityStars_app/city.html', context=context_dict)



def add_post(request, city_slug):
    return render(request, "CityStars_app/add_post.html")


def friend_feed(request):
    return render(request, "CityStars_app/friend_feed.html")


def city_feed(request):
    return render(request, "CityStars_app/city_feed.html")


def profile(request, profile_slug):
    context_dict = {}

    profile = Profile.objects.filter(slug=profile_slug)[0]

    context_dict["profile"] = profile

    return render(request, "CityStars_app/profile.html", context=context_dict)


def delete_profile(request, profile_username):
    return render(request, "CityStars_app/delete_profile.html")


def friends(request, profile_username):
    return render(request, "CityStars_app/friends.html")


def chat(request, profile_username, friend_username):
    return render(request, "CityStars_app/chat.html")


def posts(request, profile_username):
    return render(request, "CityStars_app/posts.html")


def city_post(request, city_slug, post_id):
    return render(request, "CityStars_app/city_post.html")


def user_post(request, profile_username, post_id):
    return render(request, "CityStars_app/user_post.html")


def delete_post(request, post_id):
    return render(request, "CityStars_app/delete_post.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("CityStars_app:city_stars"))
            else:
                return HttpResponse("Your account has been disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return render(
                request,
                "CityStars_app/login.html",
                {
                    "error_message": "Invalid login details supplied. Please check your username and password."
                },
            )

    return render(request, "CityStars_app/login.html")


def signup(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
            login(request, user)
            return redirect(reverse("CityStars_app:city_stars"))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render(
        request,
        "CityStars_app/register.html",
        {"user_form": user_form, "registered": registered},
    )
