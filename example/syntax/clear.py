import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

graph = Neo4jGraph( 
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
)

def reset_database(graph):
    """
    데이터베이스 초기화하기
    """
    # 모든 노드와 관계 삭제
    graph.query("MATCH (n) DETACH DELETE n")
    
    # 모든 제약조건 삭제
    constraints = graph.query("SHOW CONSTRAINTS")
    for constraint in constraints:
        constraint_name = constraint.get("name")
        if constraint_name:
            graph.query(f"DROP CONSTRAINT {constraint_name}")
    
    # 모든 인덱스 삭제
    indexes = graph.query("SHOW INDEXES")
    for index in indexes:
        index_name = index.get("name")
        index_type = index.get("type")
        if index_name and index_type != "CONSTRAINT":
            graph.query(f"DROP INDEX {index_name}")
    
    print("데이터베이스가 초기화되었습니다.")

# 데이터베이스 초기화
reset_database(graph)