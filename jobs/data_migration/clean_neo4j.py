from neomodel import config, db
admin = 'neo4j'
pw = '' # enter your pw here !! 
config.DATABASE_URL = 'bolt://%s:%s@localhost:7687' % (admin, pw)

db.cypher_query('MATCH ()-[r]-() DELETE r')
db.cypher_query('MATCH (a) DELETE a')
