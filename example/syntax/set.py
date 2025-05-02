import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

graph = Neo4jGraph( 
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
)

def set_data():
    # 노드 속성 업데이트 (SET 구문 사용)
    cypher_query = """
    // Person 레이블을 가진 노드 중에서 name 속성이 "홍길동"인 노드를 찾습니다
    // {name: "홍길동"} 형태로 속성 조건을 지정하여 특정 노드를 선택합니다
    MATCH (p:Person {name: "홍길동"})

    // SET 구문을 사용하여 찾은 노드의 속성을 업데이트합니다
    // p.age = 35: 'p'로 참조된 노드의 'age' 속성 값을 35로 설정합니다
    // 해당 속성이 이미 존재하면 값을 변경하고, 없으면 새로 생성합니다
    SET p.age = 35

    // 업데이트된 노드를 결과로 반환합니다
    // 이를 통해 변경 사항이 제대로 적용되었는지 확인할 수 있습니다
    RETURN p
    """
    # graph.query()를 사용하여 작성한 Cypher 쿼리를 Neo4j 데이터베이스에서 실행합니다
    # 결과로 속성이 업데이트된 홍길동 노드가 반환됩니다
    result = graph.query(cypher_query)
    
    # 쿼리 실행 결과를 콘솔에 출력
    print("노드 조회 결과:")
    for record in result:
        print(record)
        
set_data()