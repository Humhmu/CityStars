import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','CityStars_project.settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from CityStars_app.models import City,Post,Friendship,Profile,Chat,Message
from datetime import datetime,timezone

cities = {
    "Edinbrugh" : {
        "country":"Scotland",
        "rating": 4,
        "image": "test.png"
    },
    "Glasgow" : {
        "country":"Scotland",
        "rating": 4,
        "image": "test.png"
    },
    "London" : {
        "country":"England",
        "rating": 4,
        "image": "test.png"
    },
}
users = {
    "John125":{
        "email": "John125@mail.test",
        "profile_picture": "test.png",
        "bio": "I love looking around cities and i am a keen photographer.",
        "verified": False
    },
    "kim89" : {
        "email": "kim89@mail.test",
        "profile_picture": "test.png",
        "bio": "I am a fan of many cities and i like looking at and talking about cities.",
        "verified": False
    },
    "Julia1" : {
        "email": "Julia1@mail.test",
        "profile_picture": "test.png",
        "bio": "I am a proffesional city reveiwer and i have been to every city in the world.",
        "verified": True
    },
}

posts = [
    {
        "city":"Edinbrugh",
        "user":"John125",
        "date": datetime(year=2025,month=2,day = 14,hour=12,minute=30,tzinfo=timezone.utc),
        "image": "test.png",
        "text": "Very Nice - lots of streets and many houses! very fun!",
        "rating":4
    },
    {
        "city":"Edinbrugh",
        "user":"Julia1",
        "date": datetime(year=2025,month=2,day = 12,hour=11,minute=3,tzinfo=timezone.utc),
        "image": "test.png",
        "text": "With the city's skyline, cobbled streets and colourful characters as your backdrop, there's so many ways to embrace, explore, have fun and create lasting memories in Edinburgh",
        "rating":5
    },
    {
        "city":"Glasgow",
        "user":"Julia1",
        "date": datetime(year=2025,month=1,day = 6,hour=13,minute=45,tzinfo=timezone.utc),
        "image": "test.png",
        "text": "Glasgow has an incredible architectural heritage, set within a city full of parks and green spaces.",
        "rating":4
    },
]

freindships = {
    ("John125","kim89") : { 
        "pending" : False,
        "chat" : [
                    {
                        "sent_by":"John125",
                        "date": datetime(year=2025,month=1,day = 3,hour=21,minute=10,tzinfo=timezone.utc),
                        "text": "Hey there!"
                    },
                    {
                        "sent_by":"kim89",
                        "date": datetime(year=2025,month=1,day = 3,hour=21,minute=11,tzinfo=timezone.utc),
                        "text": "hello!"
                    },
                    {
                        "sent_by":"John125",
                        "date": datetime(year=2025,month=1,day = 3,hour=21,minute=13,tzinfo=timezone.utc),
                        "text": "i really liked your latest post!"
                    },
                ]
    },
    ("kim89","Julia1") : { 
        "pending" : False,
        "chat" :[
                    {
                        "sent_by":"kim89",
                        "date": datetime(year=2025,month=2,day = 8,hour=11,minute=45,tzinfo=timezone.utc),
                        "text": "Glasgow is a city in the west of scotland"
                    },
                    {
                        "sent_by":"Julia1",
                        "date": datetime(year=2025,month=3,day = 15,hour=20,minute=6,tzinfo=timezone.utc),
                        "text": "Yes."
                    },
                ]
    },
}



def populate():
    for city_name in cities.keys():
        cities[city_name]["object"] = add_city(city_name,cities[city_name])

    for username in users.keys():
        users[username]["object"] = add_user(username,users[username])

    for post in posts:
        post["object"] = add_post(post)

    for freindship in freindships.keys():
        freindships[freindship]["object"] = add_freindship(freindship,freindships[freindship])

        if "chat" in freindships[freindship]:
            chat = add_chat(freindships[freindship]["object"])

            for message in freindships[freindship]["chat"]:
                add_message(chat,message)

def add_city(name,details):
    k = City.objects.get_or_create(
        name = name,
        country = details["country"],
        avg_rating = details["rating"],
        image = ImageFile(open( details["image"], "rb"))
        )[0]

    k.save()
    return k

def add_user(name,details):
    u = get_user_model().objects.create_user(username = name,password = "test",email = details["email"])
    k = Profile.objects.get_or_create(
        user = u,
        bio = details["bio"],
        profile_picture = ImageFile(open( details["profile_picture"], "rb")),
        is_verified = details["verified"]
        )[0]

    k.save()
    return k

def add_post(details):
    k = Post.objects.get_or_create(
        city = cities[details["city"]]["object"],
        user = users[details["user"]]["object"],
        posted_date = details["date"],
        image = ImageFile(open( details["image"], "rb")),
        text = details["text"],
        avg_rating = details["rating"]
        )[0]

    k.save()
    return k

def add_freindship(freindship,details):
    k = Friendship.objects.get_or_create(
        user_initiated = users[freindship[0]]["object"],
        user_requested = users[freindship[1]]["object"],
        pending = details["pending"]
        )[0]

    k.save()
    return k

def add_chat(friendship):
    k = Chat.objects.get_or_create(
        friendship = friendship
        )[0]

    k.save()
    return k

def add_message(chat,details):
    k = Message.objects.get_or_create(
        chat = chat,
        user = users[details["sent_by"]]["object"],
        sent_date = details["date"],
        text = details["text"]
        )[0]

    k.save()
    return k




if __name__ == "__main__":
    print("Populating Database")
    populate()
    print("Populating Complete")