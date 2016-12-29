from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipFrom)
from django.utils import timezone




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
