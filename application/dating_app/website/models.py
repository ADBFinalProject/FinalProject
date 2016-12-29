from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField


class Dater(AbstractUser):
    AbstractUser.username = models.CharField(max_length=30)
    AbstractUser.password = models.CharField(max_length=30)
    description = models.TextField()
    gender_choices = (("w", "Women"), ("m", "Men"))
    gender = models.CharField(max_length=10, choices=gender_choices)
    sexual_orientation_choices = (("straight", "Straight"), ("bisexual", "Bisexual"), ("gay", "Gay"))
    sexual_orientation = models.CharField(max_length=10, choices=sexual_orientation_choices)
    looking_for_choices = (("sex", "Casual sex"), ("friend", "Friend"), ("short_term", "Short term relationship"),
                           ("long_term", "Long term relationship"))
    looking_for = MultiSelectField(choices=looking_for_choices)
    AbstractUser.email = models.EmailField()

    def __str__(self):
        return self.username + self.description
