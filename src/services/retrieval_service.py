from typing import List, Dict, Any
from .graph_service import GraphService
from .embeddings_service import EmbeddingService
import numpy as np

class RetrievalService:
    def __init__(self):
        self.graph_service = GraphService()
        self.embedding_service = EmbeddingService()

    async def semantic_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # Generate query embedding
        query_embedding = self.embedding_service.embeddings.embed_query(query)
        
        # Search in PostgreSQL using vector similarity
        with psycopg2.connect(**self.embedding_service.db_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT content, metadata, source, 
                           1 - (embedding <=> %s::vector) as similarity
                    FROM permanent.embeddings
                    ORDER BY embedding <=> %s::vector
                    LIMIT %s
                """, (query_embedding, query_embedding, limit))
                
                results = [{
                    'content': row[0],
                    'metadata': row[1],
                    'source': row[2],
                    'similarity': float(row[3])
                } for row in cur.fetchall()]
                
        return results

    async def graph_enhanced_search(self, query: str, max_results: int = 5, depth: int = 2) -> Dict[str, Any]:
        # 1. Get initial semantic search results
        semantic_results = await self.semantic_search(query, max_results)
        
        # 2. For each result, get related nodes from graph
        enhanced_results = []
        for result in semantic_results:
            # Extract document ID from metadata
            doc_id = result['metadata'].get('id')
            if not doc_id:
                continue

            # Get connected nodes from Neo4j
            cypher_query = """
            MATCH (doc:Document {id: $doc_id})
            CALL apoc.path.subgraphNodes(doc, {
                maxLevel: $depth,
                limit: $limit
            })
            YIELD node
            RETURN node
            """
            
            graph_nodes = self.graph_service.query_graph(
                cypher_query,
                params={'doc_id': doc_id, 'depth': depth, 'limit': 10}
            )

            # Combine semantic and graph results
            result['related_nodes'] = graph_nodes
            enhanced_results.append(result)

        return {
            'query': query,
            'results': enhanced_results
        }
