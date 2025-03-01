from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=30, unique=True)
    country = models.CharField(max_length=30)
    avg_rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='city_images', blank=True)

    #note - slug based on city-country uniqueness ensured by constraint
    slug = models.SlugField(unique=True)
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name+self.country)
        super(City, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'
        ordering = ["country"]
        constraints = [
            models.UniqueConstraint(fields=['name', 'country'], name='name&countryUnique')
        ]

class Post(models.Model):
    #note - Cascade ensures if a city/User is deleted all of the posts associated will also be deleted
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images', blank=True)
    text = models.CharField(max_length=500)
    avg_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.city.name +"|"+self.user.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.CharField(max_length=1000)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
class Freindship(models.Model):
    user_initiated = models.ForeignKey(User, on_delete=models.CASCADE)
    user_requested = models.ForeignKey(User, on_delete=models.CASCADE)
    pending = models.BooleanField(default=True)

    def __str__(self):
        return self.user_initiated.username +"|"+self.user_requested.username

class Chat(models.Model):
    users = models.ManyToManyField(User)
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sent_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.user +"|"+"Message"