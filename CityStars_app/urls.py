from django.urls import path
from CityStars_app import views

app_name = "CityStars_app"

urlpatterns = [
    # Homepage
    path("", views.city_stars, name="city_stars"),
    # City urls
    path("city/<slug:city_slug>", views.city, name="city"),
    path("city/<slug:city_slug>/<int:post_id>", views.city_post, name="city_post"),
    path("city/<slug:city_slug>/add_post", views.add_post, name="add_post"),
    # Feed urls
    path("feed/city/", views.city_feed, name="city_feed"),
    path("feed/friends/", views.friend_feed, name="friend_feed"),
    # Profile urls
    path("profile/<str:profile_username>", views.profile, name="profile"),
    path(
        "profile/<str:profile_username>/delete",
        views.delete_profile,
        name="delete_profile",
    ),
    path("profile/<str:profile_username>/friends", views.friends, name="friends"),
    path(
        "profile/<str:profile_username>/friends/<str:friend_username>/chat",
        views.chat,
        name="chat",
    ),
    path("profile/<str:profile_username>/posts", views.posts, name="posts"),
    path(
        "profile/<str:profile_username>/posts/<int:post_id>",
        views.user_post,
        name="user_post",
    ),
    # Post urls
    path("post/<int:post_id>/delete", views.delete_post, name="delete_post"),
    # Account urls
    path("register", views.signup, name="register"),
    path("login", views.user_login, name="login"),
]
