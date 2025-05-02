import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

graph = Neo4jGraph( 
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
)

cypher_query = """
CREATE (n:Test {name: "Hello AuraDB"}) 
RETURN n
"""

result = graph.query(cypher_query)

print(result)