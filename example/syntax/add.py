import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

graph = Neo4jGraph( 
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
)


def add_one():

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
    
def add_mult():

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
    
# add_one()
add_mult()