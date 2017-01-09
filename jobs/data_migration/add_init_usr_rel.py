from neomodel import config, db
admin = 'neo4j'
pw = '' # enter your pw here !! 
config.DATABASE_URL = 'bolt://%s:%s@localhost:7687' % (admin, pw)


# create follow rel
db.cypher_query('MATCH (a:user), (b:user) WHERE NOT a=b and rand() > 0.75 CREATE (a)-[:FOLLOW]->(b)')

# delete redundant attributes
db.cypher_query('MATCH (a:user) REMOVE a.location')
