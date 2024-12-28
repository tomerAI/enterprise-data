from typing import List, Dict, Any, Optional
from .graph_service import GraphService
from .embedding_service import EmbeddingService
import psycopg2

class RetrievalService:
    def __init__(self):
        self.graph_service = GraphService()
        self.embedding_service = EmbeddingService()

    async def semantic_search(
        self,
        query: str,
        limit: int = 5,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Perform semantic search with similarity threshold"""
        query_embedding = self.embedding_service.generate_embeddings(query)
        
        with psycopg2.connect(**self.embedding_service.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT content, metadata, source, 
                           1 - (embedding <=> %s::vector) as similarity
                    FROM permanent.embeddings
                    WHERE 1 - (embedding <=> %s::vector) > %s
                    ORDER BY similarity DESC
                    LIMIT %s
                """, (query_embedding, query_embedding, threshold, limit))
                
                return [{
                    'content': row[0],
                    'metadata': row[1],
                    'source': row[2],
                    'similarity': float(row[3])
                } for row in cur.fetchall()]

    async def get_related_nodes(
        self,
        doc_id: str,
        depth: int = 2,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get related nodes from graph database"""
        cypher_query = """
        MATCH (doc:Document {id: $doc_id})
        CALL apoc.path.subgraphNodes(doc, {
            maxLevel: $depth,
            limit: $limit
        })
        YIELD node
        RETURN node
        """
        return self.graph_service.query_graph(
            cypher_query,
            params={'doc_id': doc_id, 'depth': depth, 'limit': limit}
        )
