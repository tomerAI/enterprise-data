from neo4j import GraphDatabase
from typing import List, Dict, Any, Optional
from core.config import settings

class GraphService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def create_node(self, label: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        """Create a single node"""
        with self.driver.session() as session:
            result = session.run(
                f"CREATE (n:{label} $props) RETURN n",
                props=properties
            )
            return result.single()["n"]

    def create_relationship(
        self,
        source_label: str,
        target_label: str,
        relationship_type: str,
        source_props: Dict[str, Any],
        target_props: Dict[str, Any],
        relationship_props: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Create relationship between nodes"""
        with self.driver.session() as session:
            try:
                cypher = """
                MERGE (source:{source_label} {id: $source_id})
                SET source += $source_props
                MERGE (target:{target_label} {id: $target_id})
                SET target += $target_props
                MERGE (source)-[r:{rel_type} $rel_props]->(target)
                RETURN source, target
                """.format(
                    source_label=source_label,
                    target_label=target_label,
                    rel_type=relationship_type
                )
                
                session.run(
                    cypher,
                    source_id=source_props['id'],
                    target_id=target_props['id'],
                    source_props=source_props,
                    target_props=target_props,
                    rel_props=relationship_props or {}
                )
                return True
            except Exception as e:
                print(f"Error creating relationship: {e}")
                return False

    def query_graph(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a Cypher query"""
        with self.driver.session() as session:
            result = session.run(query, parameters=params or {})
            return [record.data() for record in result]