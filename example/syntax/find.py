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

def where_find():
    # 조건 지정 (WHERE 구문)
    # WHERE 구문은 MATCH로 찾은 패턴에 추가 조건을 적용할 때 사용합니다
    cypher_query = """
    // Person 레이블을 가진 노드 중에서 age 속성이 30 이상이고 사는 도시가 서울인 노드 조회
    // MATCH 구문으로 Person과 City 노드 간의 LIVES_IN 관계를 찾습니다
    MATCH (p:Person)-[r:LIVES_IN]->(c:City)
    // WHERE 구문으로 조건을 지정합니다:
    // 1. p.age >= 30: Person 노드의 나이가 30 이상인 경우만 선택
    // 2. c.name = "서울": City 노드의 이름이 "서울"인 경우만 선택
    // AND 연산자를 사용하여 두 조건을 모두 만족하는 노드만 필터링합니다
    WHERE p.age >= 30 AND c.name = "서울"
    // 조건을 만족하는 Person 노드만 결과로 반환합니다
    RETURN p
    """
    # graph.query()를 사용하여 작성한 Cypher 쿼리를 Neo4j 데이터베이스에서 실행합니다
    # 결과로 나이가 30 이상이고 서울에 사는 사람 노드들이 반환됩니다
    result = graph.query(cypher_query)
    # 쿼리 실행 결과를 콘솔에 출력
    print("노드 조회 결과:")
    for record in result:
        print(record)

# naive_find()
# alias_find()
where_find()