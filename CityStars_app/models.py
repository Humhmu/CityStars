from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class City(models.Model):
    name = models.CharField(max_length=30, unique=True)
    country = models.CharField(max_length=30)
    avg_rating = models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(1)])
    image = models.ImageField(upload_to="city_images", blank=True)

    desc = models.CharField(max_length=300,default="")
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_images", blank=True)
    bio = models.CharField(max_length=1000)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return "Profile| "+self.user.username


class Post(models.Model):
    # note - Cascade ensures if a city/User is deleted all of the posts associated will also be deleted
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="post_images", blank=True)
    text = models.CharField(max_length=500)
    title = models.CharField(max_length=15,default="")
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
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return "Message| "+str(self.user)
