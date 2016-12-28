import json
from py2neo import Graph, Node, Relationship

graph = Graph(password="password") # enter your neo4j admin pw here

#ALL_USR_FILE = '/home/andrew/workspace/usr_data/all_users_cleaned.json'
ALL_USR_FILE = '/home/andrew/workspace/usr_data/users_with_coordinate.json'
ALL_USR_json = json.loads(open(ALL_USR_FILE).read())

ks = ["picture", "orientation", "user_url", "gender", "age", "rel_status", "location", "generated_location", "id", "entertainement", "we_behavior", "essentials", "summary", "thinkings", "messaging_conditions"]
for user in ALL_USR_json.keys():
        for k in ks:
                if k not in ALL_USR_json[user].keys():
                        ALL_USR_json[user][k] = ''

tx = graph.begin()
for user in ALL_USR_json.keys():
        print user ,type( ALL_USR_json[user]['generated_location'])
        user_node = Node('user',
                         user_id = user,
                         orientation = ALL_USR_json[user]['orientation'],
                         user_url=ALL_USR_json[user]['user_url'],
                         gender=ALL_USR_json[user]['gender'],
                         age=ALL_USR_json[user]['age'],
                         rel_status=ALL_USR_json[user]['rel_status'],
                         location=ALL_USR_json[user]['location'],
                         generated_location=ALL_USR_json[user]['generated_location'],
                         id=ALL_USR_json[user]['id'],
                         entertainement=ALL_USR_json[user]['entertainement'],
                         we_behavior=ALL_USR_json[user]['we_behavior'],
                         essentials=ALL_USR_json[user]['essentials'],
                         summary=ALL_USR_json[user]['summary'],
                         thinkings=ALL_USR_json[user]['thinkings'],
                         messaging_conditions=ALL_USR_json[user]['messaging_conditions']
                         )

        for look in ALL_USR_json[user]['looking_for']:
                if look == 'age':
                        #user_node.add_label(ALL_USR_json[user]['looking_for']['age'])
                        continue
                if ALL_USR_json[user]['looking_for'][look]:
                        user_node.add_label(look)
        tx.create(user_node)
tx.commit()

