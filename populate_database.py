
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','CityStars_project.settings')
import django
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from CityStars_app.models import City,Post,Friendship,Profile,Chat,Message
from datetime import datetime,timezone
import json

def populate():
    with open("population resources/populationData.json","r") as f:
        data = json.loads(f.read())
    
    ##ADD DEFALUT PROFILE PICTURE
    add_user("DEFAULT",{"bio":"","email":"","verified":False,"profile_picture":"static\images\DEFAULT_profile_photo.jpg"})

    for city_name_country in data["cities"].keys():
        data["cities"][city_name_country]["object"] = add_city(city_name_country,data["cities"][city_name_country])

    for username in data["users"].keys():
        data["users"][username]["object"] = add_user(username,data["users"][username])

    for post in data["posts"]:
        post["object"] = add_post(post,data["users"],data["cities"])

    for freindship in data["freindships"].keys():
        data["freindships"][freindship]["object"] = add_freindship(freindship,data["freindships"][freindship],data["users"])

        if "chat" in data["freindships"][freindship]:
            chat = add_chat(data["freindships"][freindship]["object"])

            for message in data["freindships"][freindship]["chat"]:
                add_message(chat,message,data["users"])

def add_city(name_country,details):
    name,country = name_country.split("%")
    k = City.objects.get_or_create(
        name = name,
        country = country,
        avg_rating = details["rating"],
        desc = details["desc"],
        image = ImageFile(open( details["image"], "rb"),name = name+country+"_city_photo.jpg")
        )[0]

    k.save()
    return k

def add_user(name,details):
    u = get_user_model().objects.create_user(username = name,password = "test",email = details["email"])
    k = Profile.objects.get_or_create(user=u)[0]

    k.bio = details["bio"]
    k.is_verified = details["verified"]
    k.profile_picture = ImageFile(open( details["profile_picture"], "rb"),name = name+"_profile_photo.jpg")

    k.save()
    return k

def add_post(details,users,cities):
    k = Post.objects.get_or_create(
        city = cities["%".join(details["city"])]["object"],
        user = users[details["user"]]["object"],
        posted_date = datetime.fromtimestamp(details["date"],tz=timezone.utc),
        image = ImageFile(open( details["image"], "rb"),name = "post_photo.jpg"),
        text = details["text"],
        title = details["title"],
        rating = details["rating"]
        )[0]
    
    for name in details["liked_by"]:
        k.liked_by.add(users[name]["object"].user)

    k.save()
    return k

def add_freindship(freindship,details,users):
    freindInt,friendReq = freindship.split("%")
    k = Friendship.objects.get_or_create(
        user_initiated = users[freindInt]["object"],
        user_requested = users[friendReq]["object"],
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

def add_message(chat,details,users):
    k = Message.objects.get_or_create(
        chat = chat,
        user = users[details["sent_by"]]["object"],
        sent_date = datetime.fromtimestamp(details["date"],tz=timezone.utc),
        text = details["text"]
        )[0]

    k.save()
    return k




if __name__ == "__main__":
    print("Populating Database")
    populate()
    print("Populating Complete")