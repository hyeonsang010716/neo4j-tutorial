import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

graph = Neo4jGraph( 
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
)

def naive_find():
    # 노드 조회 (RETURN 구문)
    cypher_query = """
    // Person 레이블을 가진 모든 노드 조회
    // MATCH: 그래프 데이터베이스에서 특정 패턴을 찾는 명령어
    // (p:Person): p라는 변수에 Person 레이블을 가진 모든 노드를 할당
    MATCH (p:Person)

    // RETURN: 쿼리 결과로 반환할 데이터를 지정하는 명령어
    // p: Person 노드 전체(모든 속성 포함)를 반환
    RETURN p
    """
    # graph.query(): Neo4j 데이터베이스에 Cypher 쿼리를 실행하는 메서드
    result = graph.query(cypher_query)

    # 쿼리 실행 결과를 콘솔에 출력
    print("노드 조회 결과:")
    for record in result:
        print(record)

def alias_find():
    # 노드 조회 (속성 반환)
    # Person 노드의 이름 속성만 선택적으로 반환하는 쿼리 실행
    cypher_query = """
    // Person 레이블을 가진 모든 노드의 name 속성 조회
    // MATCH: 그래프 데이터베이스에서 특정 패턴을 찾는 명령어
    MATCH (p:Person)

    // RETURN: 쿼리 결과로 반환할 데이터를 지정
    // p.name: Person 노드의 name 속성만 선택적으로 반환
    // AS Name: 결과 컬럼의 이름을 'Name'으로 지정 (별칭 부여)
    RETURN p.name AS Name
    """
    # Neo4j 데이터베이스에 Cypher 쿼리를 실행하고 결과를 result 변수에 저장
    result = graph.query(cypher_query)

    # 쿼리 실행 결과를 콘솔에 출력
    print("노드 조회 결과:")
    for record in result:
        print(record)

# naive_find()
alias_find()