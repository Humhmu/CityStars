from django.urls import path, re_path
from CityStars_app.consumers import ChatConsumer

# Here, "" is routing to the URL ChatConsumer which
# will handle the chat functionality.
websocket_urlpatterns = [
    re_path(
        r"city_stars/profile/(?P<profile_slug>\w+)/friends/(?P<friend_slug>\w+)/chat/$",
        ChatConsumer.as_asgi(),
    ),
]
