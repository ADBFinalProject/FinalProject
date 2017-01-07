import json
from py2neo import Graph, Node, Relationship

graph = Graph(password="ErplEck1692")  # enter your admin pw here

ALL_USR_FILE = '../../data/users_with_coordinate.json'
ALL_USR_json = json.loads(open(ALL_USR_FILE).read())

glocations = []
with open("../../data/location.txt") as glocation_file:
    for glocation in glocation_file:
	loc = glocation.replace('\n', '').replace('\r','')
	glocations.append(loc)

#create user relationship with location
txrel = graph.begin()
for user in ALL_USR_json.keys():
    user_node = graph.find_one('user', property_key='user_id', property_value=user)
    for gloc in glocations:
        if gloc in user_node['location']:
            user_gloc = graph.find_one('glocation', property_key='user_glocation', property_value=gloc)
            print user_gloc, user_node['location']
            rel = Relationship(user_node, 'IS LOCATED AT', user_gloc)
            txrel.create(rel)
            break
txrel.commit()
