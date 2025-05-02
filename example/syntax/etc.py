import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

graph = Neo4jGraph( 
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
)

def order_and_limit():
    # 나이 순 정렬 - ORDER BY와 LIMIT 사용 예제
    cypher_query = """
    // Person 레이블을 가진 모든 노드를 찾습니다
    // 이는 데이터베이스에서 Person으로 분류된 모든 개체를 검색합니다
    MATCH (p:Person)

    // 찾은 Person 노드 전체를 결과로 반환합니다
    // 노드의 모든 속성과 레이블 정보가 포함됩니다
    RETURN p

    // ORDER BY 절을 사용하여 결과를 정렬합니다
    // p.age: Person 노드의 age 속성을 기준으로 정렬
    // ASC: 오름차순 정렬 (작은 값에서 큰 값 순서로 정렬)
    // DESC를 사용하면 내림차순 정렬이 됩니다 (큰 값에서 작은 값 순서로)
    ORDER BY p.age ASC

    // LIMIT 절을 사용하여 반환되는 결과의 수를 제한합니다
    // 여기서는 최대 2개의 결과만 반환합니다
    // 이는 가장 나이가 어린 2명의 Person만 반환하게 됩니다
    LIMIT 2
    """

    # Neo4j 데이터베이스에 Cypher 쿼리를 실행합니다
    result = graph.query(cypher_query)

    # 쿼리 결과를 순회하면서 각 레코드를 출력합니다
    print("나이 순 정렬 결과:")

    for record in result:
        print(record)
        

def skip():
    # 나이 순 정렬 (SKIP 사용)
    cypher_query = """
    // Person 레이블을 가진 모든 노드를 찾습니다
    // 이는 데이터베이스에서 Person으로 분류된 모든 개체를 검색합니다
    MATCH (p:Person)

    // 찾은 Person 노드 전체를 결과로 반환합니다
    // 노드의 모든 속성과 레이블 정보가 포함됩니다
    RETURN p

    // ORDER BY 절을 사용하여 결과를 정렬합니다
    // p.age: Person 노드의 age 속성을 기준으로 정렬
    // ASC: 오름차순 정렬 (작은 값에서 큰 값 순서로 정렬)
    ORDER BY p.age ASC

    // SKIP 절을 사용하여 결과의 처음 1개를 건너뜁니다
    // 이는 나이가 가장 어린 첫 번째 사람을 제외하고 결과를 반환합니다
    SKIP 1

    // LIMIT 절을 사용하여 반환되는 결과의 수를 제한합니다
    // 여기서는 최대 1개의 결과만 반환합니다
    // SKIP과 함께 사용하면 두 번째로 나이가 어린 사람만 반환하게 됩니다
    LIMIT 1
    """
    result = graph.query(cypher_query)
    print("나이 순 정렬 결과:")
    for record in result:
        print(record)
        
        
# order_and_limit()
skip()