import json
from py2neo import Graph, Node, Relationship

graph = Graph(password="")  # enter your admin pw here

ALL_USR_FILE = '../../data/users_with_coordinate.json'
ALL_USR_json = json.loads(open(ALL_USR_FILE).read())

#add glocation node
glocations = []
with open("../../data/location.txt") as glocation_file:
    for glocation in glocation_file:    
        loc = glocation.replace('\n', '').replace('\r','')
        glocations.append(loc)

loc_nodes = {}
txloc = graph.begin()
for glocation in glocations:
    glocation_node = Node('glocation', user_glocation=glocation)
    txloc.create(glocation_node)
    glocation_node.add_label(glocation)
    loc_nodes[glocation] = glocation_node
    print glocation_node
txloc.commit()

rels = []
rels.append(Relationship(loc_nodes['Taipei'], 'NEAR', loc_nodes['Taouyan'], dist=55))
rels.append(Relationship(loc_nodes['Taouyan'], 'NEAR', loc_nodes['Hsinchu'], dist=54))
rels.append(Relationship(loc_nodes['Hsinchu'], 'NEAR', loc_nodes['Taichung'], dist=106))
rels.append(Relationship(loc_nodes['Taichung'], 'NEAR', loc_nodes['Nantou'], dist=54))
rels.append(Relationship(loc_nodes['Taichung'], 'NEAR', loc_nodes['Tainan'], dist=168))
rels.append(Relationship(loc_nodes['Tainan'], 'NEAR', loc_nodes['Kaohsiung'], dist=49))
rels.append(Relationship(loc_nodes['Kaohsiung'], 'NEAR', loc_nodes['Taitung'], dist=172))
rels.append(Relationship(loc_nodes['Hualien'], 'NEAR', loc_nodes['Taitung'], dist=164))
rels.append(Relationship(loc_nodes['Yilan'], 'NEAR', loc_nodes['Hualien'], dist=118))
rels.append(Relationship(loc_nodes['Taipei'], 'NEAR', loc_nodes['Yilan'], dist=63))

tx_near = graph.begin()
for link in rels:
    tx_near.create(link)
tx_near.commit()


#add user node
ks = ["picture", "orientation", "user_url", "gender", "age", "rel_status", "location", "generated_location", "id", "entertainement", "we_behavior", "essentials", "summary", "thinkings", "messaging_conditions"]
for user in ALL_USR_json.keys():
        for k in ks:
                if k not in ALL_USR_json[user].keys():
                        ALL_USR_json[user][k] = ''
txuser = graph.begin()
for user in ALL_USR_json.keys():
        print user
        coordinate=ALL_USR_json[user]['generated_location'].split()[0]
        coordinates = ALL_USR_json[user]['generated_location'].split(',')
        user_node = Node('user',
                         user_id=user,
                         orientation=ALL_USR_json[user]['orientation'],
                         user_url=ALL_USR_json[user]['user_url'],
                         gender=ALL_USR_json[user]['gender'],
                         age=ALL_USR_json[user]['age'],
                         rel_status=ALL_USR_json[user]['rel_status'],
                         location=ALL_USR_json[user]['generated_location'].split()[1],
                         #generated_location=coordinate,
                         longitude=float(coordinates[3]),
                         latitude=float(coordinates[1]),
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
        txuser.create(user_node)
txuser.commit()
