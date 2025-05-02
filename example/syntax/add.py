import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

graph = Neo4jGraph( 
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
)


def add_node_one():

    cypher_query = """
    // 노드 레이블 : Person (사람을 나타내는 레이블)
    // 노드 속성 정의:
    //   - name: "홍길동" (이름)
    //   - age: 30 (나이)
    //   - email: "hong@example.com" (이메일 주소)
    // p는 생성된 노드를 참조하는 변수명입니다.
    CREATE (p:Person {name: "홍길동", age: 30, email: "hong@example.com"})
    """

    graph.query(cypher_query)

    result = graph.query(cypher_query)

    print(result)
    
def add_node_mult():

    cypher_query = """
    // 노드 레이블 정의:
    //   - Person: 사람을 나타내는 레이블
    //   - City: 도시를 나타내는 레이블
    // 
    // Person 노드 속성 정의:
    //   - name: 사람의 이름 (문자열)
    //   - age: 사람의 나이 (숫자)
    //
    // City 노드 속성 정의:
    //   - name: 도시 이름 (문자열)
    //   - population: 인구수 (숫자)
    //
    // 변수 a, b, c는 각각 생성된 노드를 참조하는 변수명입니다.
    CREATE
    (a:Person {name: "김철수", age: 25}),
    (b:Person {name: "이영희", age: 28}),
    (c:City {name: "서울", population: 9700000})
    """

    graph.query(cypher_query)

    result = graph.query(cypher_query)

    print(result)

def add_relation():
    # 기존 노드 사이에 관계 생성하기
    cypher_query = """
    // 관계 레이블 : KNOWS (알고 있다는 관계를 나타냄)
    // 관계 속성 : since (관계가 시작된 시점을 나타내는 속성)
    // 관계 방향 : a -> b (홍길동이 김철수를 알고 있는 방향성)
    // 관계 속성 값: since: 2020 (2020년부터 관계가 시작됨)
    // 관계 생성 의미 : 홍길동은 김철수를 2020년부터 알게 됨

    // MATCH 구문으로 두 개의 기존 노드를 찾음
    MATCH 
    (a:Person {name: "홍길동"}),  // Person 레이블을 가진 이름이 홍길동인 노드를 찾아 변수 a에 할당
    (b:Person {name: "김철수"})   // Person 레이블을 가진 이름이 김철수인 노드를 찾아 변수 b에 할당

    // CREATE 구문으로 두 노드 사이에 방향성 있는 관계 생성
    CREATE (a)-[r:KNOWS {since: 2020}]->(b)  // a에서 b로 향하는 KNOWS 타입의 관계 r 생성, since 속성 추가

    // RETURN 구문으로 노드와 관계 정보 반환
    RETURN a, b, r  // 생성된 관계와 연결된 두 노드 정보를 함께 반환
    """
    # Neo4j 데이터베이스에 Cypher 쿼리를 실행하여 두 노드 간 관계를 생성
    graph.query(cypher_query)

def add_node_relation():
    # 노드와 관계를 한 번에 생성하는 Cypher 쿼리
    cypher_query = """
    // 노드 레이블 : Person, City (각각 사람과 도시를 나타내는 레이블)
    // CREATE 구문으로 노드와 관계를 동시에 생성
    CREATE 
    // a 변수에 Person 레이블을 가진 노드 생성, 속성으로 name="박지성" 설정
    (a:Person {name: "박지성"})-[:LIVES_IN]->
    // c 변수에 City 레이블을 가진 노드 생성, 속성으로 name="맨체스터" 설정
    // LIVES_IN 관계는 '살고 있다'는 의미로 박지성이 맨체스터에 거주함을 나타냄
    (c:City {name: "맨체스터"})
    // RETURN 구문으로 생성된 두 노드 정보 반환
    RETURN a, c
    """
    # Neo4j 데이터베이스에 Cypher 쿼리를 실행하여 노드와 관계를 동시에 생성
    graph.query(cypher_query)

# add_node_one()
# add_node_mult()
# add_relation()
add_node_relation()