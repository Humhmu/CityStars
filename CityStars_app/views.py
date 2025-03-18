from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from CityStars_app.forms import UserForm, PostForm
from django.contrib.auth import authenticate, login, logout
from CityStars_app.models import *
import datetime
from django.contrib.auth.decorators import login_required


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
        context_dict["city"] = city

        context_dict["top_posts"] = Post.objects.filter(city=city).order_by("-likes")[
            :3
        ]
    except City.DoesNotExist:
        context_dict["city"] = None

    return render(request, "CityStars_app/city.html", context=context_dict)


def add_post(request, city_slug):
    city = City.objects.filter(slug=city_slug)[0]
    cities = City.objects.get_queryset()

    if request.method == "POST":
        profile = Profile.objects.filter(user=request.user)[0]
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.city = city
            newpost.user = profile
            newpost.save()
            return redirect(reverse("CityStars_app:city_stars"))
        else:
            return render(
                request,
                "CityStars_app/add_post.html",
                {"city": city, "cities": cities, "form": form},
            )
    else:
        form = PostForm()

    return render(
        request,
        "CityStars_app/add_post.html",
        {"form": form, "city": city, "cities": cities},
    )


def friend_feed(request):
    context_dict = {}
    context_dict["posts"] = []

    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user = user)

        friends = [
            o.user_requested if o.user_requested != profile else o.user_initiated
            for o in Friendship.objects.filter(user_initiated=profile)
            | Friendship.objects.filter(user_requested=profile)
        ]
        print(friends)
        
        for friend in friends:
            context_dict["posts"] += Post.objects.filter(user = friend).order_by('-posted_date')
            print(context_dict["posts"])
    return render(request, "CityStars_app/friend_feed.html", context=context_dict)


def city_feed(request):
    context_dict = {}

    context_dict["posts"] = Post.objects.order_by("-posted_date")

    return render(request, "CityStars_app/city_feed.html", context=context_dict)


def profile(request, profile_slug):
    context_dict = {}

    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user = user)
        profile = Profile.objects.filter(slug = profile_slug)[0]
        context_dict["friend"] = any([
                (
                    True
                    if o.user_requested == profile or o.user_initiated == profile
                    else False
                )
                for o in Friendship.objects.filter(user_initiated=user_profile)
                | Friendship.objects.filter(user_requested=user_profile)
            ])
        context_dict["profile"] = profile

        return render(request, "CityStars_app/profile.html", context=context_dict)
    else:
        return redirect('CityStars_app:login')


def delete_profile(request, profile_slug):
    return render(request, "CityStars_app/delete_profile.html")


def friends(request, profile_slug):
    context_dict = {}

    user = request.user
    if user.is_authenticated and user.profile.slug == profile_slug:
        profile = Profile.objects.get(user = user)
        context_dict["profile"] = profile
        context_dict["friends"] = [
            (
                o.user_requested
                if o.user_requested != profile
                else o.user_initiated
            )
            for o in Friendship.objects.filter(user_initiated=profile)
            | Friendship.objects.filter(user_requested=profile)
        ]
        for o in context_dict["friends"]:
            o.numberOfPosts = len(Post.objects.filter(user=o))

        return render(request, "CityStars_app/friends.html", context=context_dict)
    else:
        return redirect('CityStars_app:city_stars')
    


def chat(request, profile_slug, friend_slug):
    return render(request, "CityStars_app/chat.html")


def posts(request, profile_slug):
    context_dict = {}

    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(slug = profile_slug)
        context_dict["user_posts"] = Post.objects.filter(user=profile)
        context_dict["profile"] = profile
        print(context_dict)
        return render(request, "CityStars_app/posts.html",context=context_dict)
    else:
        return redirect('CityStars_app:login')


def post(request, post_id):
    context_dict = {}

    try:
        post = Post.objects.get(id=post_id)
        city = post.city
        context_dict["city_name"] = city.name
        context_dict["city_post_id"] = post
    except (City.DoesNotExist, Post.DoesNotExist):
        context_dict["city_name"] = None
        context_dict["city_post_id"] = None

    return render(request, "CityStars_app/post.html", context_dict)

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

@login_required
def user_logout(request):
    logout(request)

    return redirect(reverse("CityStars_app:city_stars"))

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
