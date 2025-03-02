from django.http import HttpResponse


def cityStars(request):
    return HttpResponse("Homepage")


def city(request):
    return HttpResponse("City Page")


def addPost(request):
    return HttpResponse("Add Post Page")


def friendFeed(request):
    return HttpResponse("Friend Feed Page")


def cityFeed(request):
    return HttpResponse("City Feed Page")


def profile(request):
    return HttpResponse("Profile Page")


def friends(request):
    return HttpResponse("Friends Page")


def chat(request):
    return HttpResponse("Chat Page")


def posts(request):
    return HttpResponse("Posts Page")


def login(request):
    return HttpResponse("Login Page")


def signup(request):
    return HttpResponse("Signup Page")
