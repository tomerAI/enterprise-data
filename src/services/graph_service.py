from neo4j import GraphDatabase
from typing import List, Dict, Any
from core.config import settings

class GraphService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def create_graph_elements(self, elements: List[Dict[str, Any]]) -> int:
        """Create nodes and relationships from processed CSV data"""
        records_processed = 0
        
        with self.driver.session() as session:
            for element in elements:
                try:
                    cypher = """
                    MERGE (source:{source_label} {id: $source})
                    SET source += $source_properties
                    MERGE (target:{target_label} {id: $target})
                    SET target += $target_properties
                    MERGE (source)-[r:{relationship} $relationship_properties]->(target)
                    RETURN source, target
                    """.format(
                        source_label=element['source'].split(':')[0],
                        target_label=element['target'].split(':')[0],
                        relationship=element['relationship']
                    )
                    
                    session.run(
                        cypher,
                        source=element['source'],
                        target=element['target'],
                        source_properties=element['source_properties'],
                        target_properties=element['target_properties'],
                        relationship_properties=element['relationship_properties']
                    )
                    records_processed += 1
                except Exception as e:
                    print(f"Error processing graph element: {e}")
                    
        return records_processed