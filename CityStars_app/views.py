from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from CityStars_app.forms import UserForm, PostForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from CityStars_app.models import *
import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def city_stars(request):
    context_dict = {}
    context_dict["cities"] = City.objects.filter(
        id__in=Post.objects.values_list("city", flat=True)
    ).distinct()

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
                    posted_date__gte=datetime.datetime.now(tz=datetime.timezone.utc)
                    - datetime.timedelta(weeks=1),
                )
            ),
        )

    return render(request, "CityStars_app/city_stars.html", context_dict)


def city(request, city_slug):
    context_dict = {}
    try:
        city = City.objects.get(slug=city_slug)
        context_dict["city"] = city

        context_dict["header"] = True
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
        profile = Profile.objects.get(user=user)

        friends = [
            o.user_requested if o.user_requested != profile else o.user_initiated
            for o in Friendship.objects.filter(user_initiated=profile, pending=False)
            | Friendship.objects.filter(user_requested=profile, pending=False)
        ]

        for friend in friends:
            context_dict["posts"] += Post.objects.filter(user=friend).order_by(
                "-posted_date"
            )

    return render(request, "CityStars_app/friend_feed.html", context=context_dict)


def city_feed(request):
    context_dict = {}

    context_dict["posts"] = Post.objects.order_by("-posted_date")
    context_dict["countries"] = City.objects.values_list(
        "country", flat=True
    ).distinct()
    context_dict["cities"] = (
        City.objects.filter(id__in=Post.objects.values_list("city", flat=True))
        .values_list("name", flat=True)
        .distinct()
    )

    return render(request, "CityStars_app/city_feed.html", context=context_dict)


def profile(request, profile_slug):
    context_dict = {}

    user = request.user
    if user.is_authenticated:

        user_profile = Profile.objects.get(user=user)
        profile = Profile.objects.filter(slug=profile_slug)[0]

        if request.method == "POST" and user_profile == profile:
            old_picture = profile.profile_picture
            form = UserProfileForm(request.POST, request.FILES, instance=profile)

            if form.is_valid():
                form.save()

        context_dict["friend"] = any(
            [
                (
                    True
                    if (o.user_requested == profile or o.user_initiated == profile)
                    and o.pending == False
                    else False
                )
                for o in Friendship.objects.filter(user_initiated=user_profile)
                | Friendship.objects.filter(user_requested=user_profile)
            ]
        )
        context_dict["pending"] = any(
            [
                (
                    True
                    if (
                        o.user_requested == profile and o.user_initiated == user_profile
                    )
                    and o.pending == True
                    else False
                )
                for o in Friendship.objects.filter(user_initiated=user_profile)
                | Friendship.objects.filter(user_requested=user_profile)
            ]
        )
        context_dict["requested"] = any(
            [
                (
                    True
                    if (o.user_requested == user_profile or o.user_initiated == profile)
                    and o.pending == True
                    else False
                )
                for o in Friendship.objects.filter(user_initiated=user_profile)
                | Friendship.objects.filter(user_requested=user_profile)
            ]
        )
        context_dict["profile"] = profile

        return render(request, "CityStars_app/profile.html", context=context_dict)
    else:
        return redirect("CityStars_app:login")


@login_required
def send_friend_request(request, profile_slug):
    sender_profile = request.user.profile
    receiver_profile = Profile.objects.filter(slug=profile_slug)[0]

    Friendship.objects.create(
        user_initiated=sender_profile, user_requested=receiver_profile
    )

    return redirect("CityStars_app:profile", profile_slug=receiver_profile.slug)


@login_required
def accept_friend_request(request, profile_slug):
    sender_profile = Profile.objects.filter(slug=profile_slug)[0]
    receiver_profile = request.user.profile

    friendship = Friendship.objects.get(
        user_initiated=sender_profile, user_requested=receiver_profile, pending=True
    )

    friendship.pending = False
    friendship.save()
    chat = Chat(friendship=friendship)
    chat.save()

    return redirect("CityStars_app:profile", profile_slug=sender_profile.slug)


@login_required
def reject_friend_request(request, profile_slug):
    sender_profile = Profile.objects.filter(slug=profile_slug)[0]
    receiver_profile = request.user.profile

    friendship = Friendship.objects.get(
        user_initiated=sender_profile, user_requested=receiver_profile, pending=True
    )

    friendship.delete()

    return redirect("CityStars_app:profile", profile_slug=sender_profile.slug)


def delete_profile(request, profile_slug):
    return render(request, "CityStars_app/delete_profile.html")


def friends(request, profile_slug):
    context_dict = {}

    user = request.user
    if user.is_authenticated and user.profile.slug == profile_slug:
        profile = Profile.objects.get(user=user)
        context_dict["profile"] = profile
        context_dict["friends"] = [
            (o.user_requested if o.user_requested != profile else o.user_initiated)
            for o in Friendship.objects.filter(user_initiated=profile, pending=False)
            | Friendship.objects.filter(user_requested=profile, pending=False)
        ]
        for o in context_dict["friends"]:
            o.numberOfPosts = len(Post.objects.filter(user=o))

        return render(request, "CityStars_app/friends.html", context=context_dict)
    else:
        return redirect("CityStars_app:login")


def chat(request, profile_slug, friend_slug):
    # Prevent user from seeing other user's chats
    if request.user.profile.slug != profile_slug:
        # TODO: take user to a "You should not be here" page
        return redirect("CityStars_app:city_stars")

    context_dict = {}
    profile = Profile.objects.filter(slug=profile_slug)[0]
    friend = Profile.objects.filter(slug=friend_slug)[0]
    friendship = Friendship.objects.filter(
        Q(user_initiated=profile, user_requested=friend)
        | Q(user_initiated=friend, user_requested=profile)
    )
    if len(friendship) > 0:
        chat = Chat.objects.filter(friendship=friendship[0])[0]
    else:
        # TODO: take user to a "You cannot chat with a user if not friends" page
        return redirect("CityStars_app:city_stars")

    messages = Message.objects.filter(chat=chat).order_by("sent_date")

    context_dict["profile"] = profile
    context_dict["friend"] = friend
    context_dict["chat"] = chat
    context_dict["messages"] = messages

    return render(request, "CityStars_app/chat.html", context_dict)


def posts(request, profile_slug):
    context_dict = {}

    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(slug=profile_slug)
        context_dict["user_posts"] = Post.objects.filter(user=profile)
        context_dict["profile"] = profile

        return render(request, "CityStars_app/posts.html", context=context_dict)
    else:
        return redirect("CityStars_app:login")


def post(request, post_id):
    context_dict = {}

    try:
        post = Post.objects.get(id=post_id)
        city = post.city
        context_dict["city"] = city
        context_dict["city_name"] = city.name
        context_dict["city_post_id"] = post
        context_dict["city_post_user"] = post.user.user.username
        context_dict["user_slug"] = post.user.slug
        context_dict["city_post_image"] = post.image
        context_dict["city_post_title"] = post.title
        context_dict["city_post_text"] = post.text
        context_dict["city_post_date"] = post.posted_date
        context_dict["post_likes"] = post.likes
        context_dict["post_rating"] = post.rating
    except (City.DoesNotExist, Post.DoesNotExist):
        context_dict["city"] = "Unknown"
        context_dict["city_name"] = "City"
        context_dict["city_post_id"] = "ID"
        context_dict["city_post_user"] = "Unknown"
        context_dict["user_slug"] = "Unknown"
        context_dict["city_post_image"] = "DEFAULT_profile_photo.jpg"
        context_dict["city_post_title"] = "Untitled"
        context_dict["city_post_text"] = "The user has not commented on this post."
        context_dict["city_post_date"] = "Date"
        context_dict["post_likes"] = 0
        context_dict["post_rating"] = 1

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
