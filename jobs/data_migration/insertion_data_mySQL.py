import os
import sys
import django
import json
sys.path.append('../../application/dating_app/website')
sys.path.append('../../application/dating_app/dating_app')
sys.path.append('../../application/dating_app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()
from website.models import Dater


ALL_USR_FILE = '../../data/users_with_coordinate.json'
users = json.loads(open(ALL_USR_FILE).read())


for user in users:
    user_details = users[user]
    user_to_insert = Dater
    user_to_insert.username = user
    if 'summary' in user_details:
        user_to_insert.summary = user_details['summary']
    if 'age' in user_details:
        user_to_insert.age = user_details['age']
    if 'entertainement' in user_details:
        user_to_insert.entertainement = user_details['entertainement']
    else:
        user_to_insert.entertainement = ""
    if 'we_behavior' in user_details:
        user_to_insert.we_behavior = user_details['we_behavior']
    else:
        user_to_insert.we_behavior = ""
    if 'essentials' in user_details:
        user_to_insert.essentials = user_details['essentials']
    else:
        user_to_insert.essentials = ""
    if 'thinkings' in user_details:
        user_to_insert.thinkings = user_details['thinkings']
    else:
        user_to_insert.thinkings = ""
    if 'messaging_conditions' in user_details:
        user_to_insert.messaging_conditions = user_details['messaging_conditions']
    else:
        user_to_insert.messaging_conditions = ""
    if 'gender' in user_details:
        if user_details['gender'] == "Woman":
            user_to_insert.gender = "w"
        else:
            user_to_insert.gender = "m"
    if 'sexual_orientation' in user_details:
        if user_details['sexual_orientation'] == "Straight":
            user_to_insert.sexual_orientation = "straight"
        elif user_details['sexual_orientation'] == "Gay":
            user_to_insert.sexual_orientation = "gay"
        else:
            user_to_insert.sexual_orientation = "bisexual"
    else:
        user_to_insert.sexual_orientation = "straight"
    user_to_insert_looking_for = []
    if "looking_for" in user_details:
        if "long_term" in user_details["looking_for"]:
            user_to_insert_looking_for.append("long_term")
        if "short_term" in user_details["looking_for"]:
            user_to_insert_looking_for.append("short_term")
        if "casual_sex" in user_details["looking_for"]:
            user_to_insert_looking_for.append("sex")
        if "friend" in user_details["looking_for"]:
            user_to_insert_looking_for.append("friend")

    user_to_insert.looking_for = user_to_insert_looking_for
    coordinates = user_details['generated_location'].split(',')
    user_to_insert.latitude = float(coordinates[1])
    user_to_insert.longitude = float(coordinates[3])
    user_to_save = Dater.objects.create_user(username=user_to_insert.username, summary=user_to_insert.summary,
                                             age=user_to_insert.age, entertainement=user_to_insert.entertainement,
                                             we_behavior=user_to_insert.we_behavior,
                                             essentials=user_to_insert.essentials, thinkings=user_to_insert.thinkings,
                                             messaging_conditions=user_to_insert.messaging_conditions,
                                             gender=user_to_insert.gender,
                                             sexual_orientation=user_to_insert.sexual_orientation,
                                             looking_for=user_to_insert.looking_for, latitude=user_to_insert.latitude,
                                             longitude=user_to_insert.longitude)
    user_to_save.set_password("blabla")
    user_to_save.save()

