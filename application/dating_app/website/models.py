from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField


class Dater(AbstractUser):
    AbstractUser.username = models.CharField(max_length=30)
    AbstractUser.password = models.CharField(max_length=30)
    picture = models.ImageField(upload_to="users_picture", blank=True, null=True)
    summary = models.TextField()
    picture_url = models.TextField()
    entertainement = models.TextField()
    we_behavior = models.TextField()
    essentials = models.TextField()
    thinkings = models.TextField()
    messaging_conditions = models.TextField()
    latitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=5, blank=True, null=True)
    gender_choices = (("w", "Women"), ("m", "Men"))
    gender = models.CharField(max_length=10, choices=gender_choices)
    sexual_orientation_choices = (("straight", "Straight"), ("bisexual", "Bisexual"), ("gay", "Gay"))
    sexual_orientation = models.CharField(max_length=10, choices=sexual_orientation_choices)
    looking_for_choices = (("sex", "Casual sex"), ("friend", "Friend"), ("short_term", "Short term relationship"),
                           ("long_term", "Long term relationship"))
    age = models.CharField(max_length=2)
    looking_for = MultiSelectField(choices=looking_for_choices)
    AbstractUser.email = models.EmailField()

    def __str__(self):
        return self.username


class Location(models.Model):
    name_of_location = models.TextField()
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)
    
    def __str__(self):
        return self.name_of_location