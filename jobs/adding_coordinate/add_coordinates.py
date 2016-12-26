# -*- coding: utf-8 -*-
"""
This script is used to add some random coordinate to the user.
Coordinates are get using a website and then save in a file.
"""

import json
import random

coordinates = []
with open("coordinates.txt") as coordinates_file:
    for coordinate in coordinates_file:
        coordinates.append(coordinate)

coordinates_with_city = []
for index, coordinate in enumerate(coordinates):
    if index <= 4000:
        coordinates_with_city.append(coordinate.replace("\n", ' Taipei'))
    elif index > 4000 and index <= 5000:
        coordinates_with_city.append(coordinate.replace("\n", ' Taichung'))
    elif index > 5000 and index <= 6000:
        coordinates_with_city.append(coordinate.replace("\n", ' Kaohsiung'))
    elif index > 6000 and index <= 6500:
        coordinates_with_city.append(coordinate.replace("\n", ' Hsinchu'))
    elif index > 6500 and index <= 7000:
        coordinates_with_city.append(coordinate.replace("\n", ' Tainan'))
    elif index > 7000 and index <= 7500:
        coordinates_with_city.append(coordinate.replace("\n", ' Taouyan'))
    elif index > 7500 and index <= 7750:
        coordinates_with_city.append(coordinate.replace("\n", ' Yilan'))
    elif index > 7750 and index <= 8000:
        coordinates_with_city.append(coordinate.replace("\n", ' Taitung'))
    elif index > 8000 and index <= 8250:
        coordinates_with_city.append(coordinate.replace("\n", ' Hualien'))
    elif index > 8000 and index <= 8500:
        coordinates_with_city.append(coordinate.replace("\n", ' Nantou'))

with open("../../data/all_users_cleaned2.json") as user_file:
    users = json.load(user_file)

coordinate_used = []

while len(coordinate_used) < len(users):
    random_coordinate = random.choice(coordinates_with_city)
    while random_coordinate in coordinate_used:
        random_coordinate = random.choice(coordinates_with_city)
    coordinate_used.append(random_coordinate.replace('\n', ''))

for index, user in enumerate(users):
    users[user]['generated_location'] = coordinate_used[index]

with open('../../data/users_with_coordinate.json', 'w') as new_user_file:
    json.dump(users, new_user_file)