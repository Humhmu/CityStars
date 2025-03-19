from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

class City(models.Model):
    CITY_MAX_LENGTH = 30
    COUNTRY_MAX_LENGTH = 30
    DESC_MAX_LENGTH = 300
    name = models.CharField(max_length=CITY_MAX_LENGTH, unique=True)
    country = models.CharField(max_length=COUNTRY_MAX_LENGTH)
    avg_rating = models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(1)])
    image = models.ImageField(upload_to="city_images", blank=True)

    desc = models.CharField(max_length=DESC_MAX_LENGTH,default="")
    # note - slug based on city-country uniqueness ensured by constraint
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + self.country)
        super(City, self).save(*args, **kwargs)

    def __str__(self):
        return "City| "+self.name

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ["country"]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country"], name="name&countryUnique"
            )
        ]


class Profile(models.Model):
    BIO_MAX_LENGTH = 1000
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_images", default="profile_images/DEFAULT_profile_photo.jpg", blank=True)
    bio = models.CharField(max_length=BIO_MAX_LENGTH, blank=True, default="No biography written")
    is_verified = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return "Profile| "+self.user.username


class Post(models.Model):
    TEXT_MAX_LENGTH = 500
    TITLE_MAX_LENGTH = 20
    # note - Cascade ensures if a city/User is deleted all of the posts associated will also be deleted
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(default=datetime.datetime.now())
    image = models.ImageField(upload_to="post_images", blank=False)
    text = models.CharField(max_length=TEXT_MAX_LENGTH, blank=False)
    title = models.CharField(max_length=TITLE_MAX_LENGTH, blank=False)
    rating = models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(1)])
    likes = models.IntegerField(default=0)

    def __str__(self):
        return "Post| "+str(self.city)+ " & " + str(self.user)


class Friendship(models.Model):
    user_initiated = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="user_initiated"
    )
    user_requested = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="user_requested"
    )
    pending = models.BooleanField(default=True)

    def __str__(self):
        return "Friendship| "+str(self.user_initiated)+ " & " + str(self.user_requested)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user_initiated", "user_requested"], name="freindshipUnique"
            )
        ]


class Chat(models.Model):
    friendship = models.ForeignKey(Friendship,on_delete=models.CASCADE,default=None)
    def __str__(self):
        return "Chat| "+str(self.friendship)

class Message(models.Model):
    MESSAGE_MAX_LENGTH = 200
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=MESSAGE_MAX_LENGTH)

    def __str__(self):
        return "Message| "+str(self.user)
