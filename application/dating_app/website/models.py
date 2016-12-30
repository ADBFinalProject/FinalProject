from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipFrom)


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
        return self.username


class User(StructuredNode):
        # basic info
        username = StringProperty(max_length=30)
        password = StringProperty(max_length=30)
        email = StringProperty()

        # details info
        picture = StringProperty()
        orientation = StringProperty()
        user_url = StringProperty()
        gender = StringProperty()   # 1 for male, 0 for female
        age = IntegerProperty()    # how old is this user
        rel_status = StringProperty()      # single or open relationship
        location = StringProperty()
        id = StringProperty()
        entertainement = StringProperty()
        we_behavior = StringProperty()
        essentials = StringProperty()
        summary = StringProperty()
        thinkings = StringProperty()
        messaging_conditions = StringProperty()
        #looking_for


        # Relationship
        following = RelationshipFrom('User', 'FOLLOWING')
        at_location = RelationshipFrom('Location', 'AT')

        def __str__(self):
                return self.username


class Location(StructuredNode):
        location_name = StringProperty()

        near = RelationshipFrom('Location', 'NEAR')
        inhabitant = RelationshipFrom('User', 'IS_FROM')

        def __str__(self):
                return self.location_name
