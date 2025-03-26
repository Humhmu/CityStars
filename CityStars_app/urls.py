from django.urls import path
from CityStars_app import views

app_name = "CityStars_app"

urlpatterns = [
    # Homepage
    path("", views.city_stars, name="city_stars"),
    # City urls
    path("city/<slug:city_slug>", views.city, name="city"),
    path("add_post", views.add_post, name="add_post"),
    # Feed urls
    path("feed/city/", views.city_feed, name="city_feed"),
    path("feed/friends/", views.friend_feed, name="friend_feed"),
    # Profile urls
    path("profile/<slug:profile_slug>", views.profile, name="profile"),
    path(
        "profile/<slug:profile_slug>/delete",
        views.delete_profile,
        name="delete_profile",
    ),
    path("profile/<slug:profile_slug>/friends", views.friends, name="friends"),
    path(
        "profile/<slug:profile_slug>/friends/<slug:friend_slug>/chat",
        views.chat,
        name="chat",
    ),
    path("profile/<slug:profile_slug>/posts", views.posts, name="posts"),
    # Post urls
    path("post/<int:post_id>/delete", views.delete_post, name="delete_post"),
    path(
        "post/posts/<int:post_id>",
        views.post,
        name="post",
    ),
    # Account urls
    path("register", views.signup, name="register"),
    path("login", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    # Friendship urls
    path(
        "profile/<slug:profile_slug>/send_friend_request/",
        views.send_friend_request,
        name="send_friend_request",
    ),
    path(
        "profile/<slug:profile_slug>/accept_friend_request/",
        views.accept_friend_request,
        name="accept_friend_request",
    ),
    path(
        "profile/<slug:profile_slug>/reject_friend_request/",
        views.reject_friend_request,
        name="reject_friend_request",
    ),
]
