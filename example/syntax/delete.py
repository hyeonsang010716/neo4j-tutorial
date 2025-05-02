import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

load_dotenv()

graph = Neo4jGraph( 
    url=os.getenv("NEO4J_URI"), 
    username=os.getenv("NEO4J_USERNAME"), 
    password=os.getenv("NEO4J_PASSWORD"),
)

def delete_node():
    try:
        # 노드 삭제 작업 수행
        cypher_query = """
        // Person 레이블을 가진 노드 중에서 name 속성이 "이영희"인 노드를 찾습니다
        // {name: "이영희"} 형태로 속성 조건을 지정하여 특정 노드를 선택합니다
        MATCH (p:Person {name: "이영희"})

        // DELETE 명령어를 사용하여 찾은 노드를 삭제합니다
        // 주의: 이 방식은 관계가 없는 노드만 삭제 가능합니다
        // 노드에 관계가 있는 경우 ConstraintValidationFailed 오류가 발생합니다
        // 관계가 있는 노드를 삭제하려면 DETACH DELETE를 사용해야 합니다
        DELETE p
        """
        # graph.query()를 사용하여 작성한 Cypher 쿼리를 Neo4j 데이터베이스에서 실행합니다
        # 결과로 이영희 노드가 삭제됩니다(단, 관계가 없는 경우에만)
        graph.query(cypher_query)
        
    except Exception as e:
        print(e)
        
def delte_node_relation():
    # 관계가 있는 노드 삭제 (DETACH DELETE 사용)
    cypher_query = """
    // Person 레이블을 가진 노드 중에서 name 속성이 "이영희"인 노드를 찾습니다
    MATCH (p:Person {name: "이영희"})

    // DETACH DELETE 명령어를 사용하여 노드와 그에 연결된 모든 관계를 함께 삭제합니다
    // 일반 DELETE와 달리 DETACH DELETE는 노드에 관계가 있어도 삭제가 가능합니다
    // 이 명령어는 먼저 노드에 연결된 모든 관계를 제거한 후 노드 자체를 삭제합니다
    // 이는 노드 삭제 시 발생할 수 있는 ConstraintValidationFailed 오류를 방지합니다
    DETACH DELETE p
    """
    # graph.query()를 사용하여 작성한 Cypher 쿼리를 Neo4j 데이터베이스에서 실행합니다
    # 결과로 이영희 노드와 그에 연결된 모든 관계가 함께 삭제됩니다
    graph.query(cypher_query)

def delete_relation():
    # 관계 삭제 작업 수행
    cypher_query = """
    // Person 레이블을 가진 노드 중에서 name 속성이 "홍길동"인 노드와 "김철수"인 노드 사이의 관계를 찾습니다
    // (a:Person {name: "홍길동"}) - 시작 노드를 a 변수에 할당하고 name이 "홍길동"인 Person 노드로 지정합니다
    // -[r]-> - 방향성이 있는 관계를 r 변수에 할당합니다 (관계 유형은 지정하지 않아 모든 유형의 관계가 대상이 됩니다)
    // (b:Person {name: "김철수"}) - 도착 노드를 b 변수에 할당하고 name이 "김철수"인 Person 노드로 지정합니다
    MATCH 
    (a:Person {name: "홍길동"})-[r]->(b:Person {name: "김철수"})

    // DELETE r 명령어를 사용하여 찾은 관계만 삭제합니다
    // 이 명령은 노드는 그대로 유지하고 두 노드 사이의 관계만 제거합니다
    // 노드 삭제와 달리 관계 삭제는 DETACH 키워드가 필요하지 않습니다
    DELETE r
    """
    # graph.query()를 사용하여 작성한 Cypher 쿼리를 Neo4j 데이터베이스에서 실행합니다
    # 결과로 홍길동과 김철수 사이의 관계가 삭제되지만 두 노드는 그대로 유지됩니다
    graph.query(cypher_query)
    
def delete_attribute():
    # 속성 제거 (REMOVE 구문 사용)
    cypher_query = """
    // Person 레이블을 가진 노드 중에서 name 속성이 "홍길동"인 노드를 찾습니다
    MATCH (p:Person {name: "홍길동"})

    // REMOVE 명령어를 사용하여 찾은 노드의 age 속성을 제거합니다
    // 이 명령은 노드 자체나 다른 속성은 그대로 유지하고 지정된 속성만 삭제합니다
    // 속성이 존재하지 않는 경우에도 오류 없이 실행됩니다
    REMOVE p.age

    // 변경된 노드를 결과로 반환합니다
    // 이를 통해 age 속성이 제거된 것을 확인할 수 있습니다
    RETURN p
    """
    # graph.query()를 사용하여 작성한 Cypher 쿼리를 Neo4j 데이터베이스에서 실행합니다
    # 결과로 홍길동 노드에서 age 속성이 제거된 노드 정보가 반환됩니다
    graph.query(cypher_query)
    
def delete_label():
    # 레이블 제거 (REMOVE 구문 사용)
    cypher_query = """
    // Person 레이블을 가진 노드 중에서 name 속성이 "홍길동"인 노드를 찾습니다
    // p 변수에 해당 노드를 할당합니다
    MATCH (p:Person {name: "홍길동"})

    // REMOVE 명령어를 사용하여 찾은 노드에서 Person 레이블을 제거합니다
    // 이 명령은 노드 자체나 속성은 그대로 유지하고 지정된 레이블만 삭제합니다
    // 레이블이 제거되면 해당 노드는 더 이상 Person으로 분류되지 않습니다
    // 노드에 다른 레이블이 있다면 그 레이블은 유지됩니다
    REMOVE p:Person

    // 변경된 노드를 결과로 반환합니다
    // 이를 통해 Person 레이블이 제거된 노드 정보를 확인할 수 있습니다
    RETURN p
    """
    # graph.query()를 사용하여 작성한 Cypher 쿼리를 Neo4j 데이터베이스에서 실행합니다
    # 결과로 홍길동 노드에서 Person 레이블이 제거된 노드 정보가 반환됩니다
    graph.query(cypher_query)
    
# delete_node()
# delte_node_relation()
# delete_relation()
# delete_attribute()
delete_label()