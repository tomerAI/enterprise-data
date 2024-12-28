from typing import List, Dict, Any
from langchain.embeddings import OpenAIEmbeddings
import hashlib
import json
from datetime import datetime
import psycopg2
from utils.db import get_db_params, wait_for_db
import os

class EmbeddingService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.db_params = get_db_params()
        if not wait_for_db(self.db_params):
            raise RuntimeError("Database connection failed")

    def generate_embeddings(self, content: str) -> List[float]:
        """Generate embeddings for a single piece of content"""
        return self.embeddings.embed_query(content)

    def process_content(self, content: str, metadata: Dict[str, Any], source: str) -> Dict[str, Any]:
        """Process a single piece of content and return document with embedding"""
        doc_hash = hashlib.md5(content.encode()).hexdigest()
        vector = self.generate_embeddings(content)
        
        return {
            "content": content,
            "embedding": vector,
            "document_hash": doc_hash,
            "metadata": metadata,
            "source": source,
            "version": "1.0",
            "processed_at": datetime.now().isoformat()
        }

    def store_embeddings(self, documents: List[Dict[str, Any]]) -> int:
        """Store embeddings in database"""
        schema = os.getenv("DBT_SCHEMA", "permanent")
        inserted_count = 0

        with psycopg2.connect(**self.db_params) as conn:
            with conn.cursor() as cur:
                for doc in documents:
                    try:
                        cur.execute("""
                            INSERT INTO {}.embeddings 
                            (content, embedding, document_hash, version, processed_at, source, metadata)
                            VALUES (%s, %s::vector, %s, %s, %s, %s, %s)
                            ON CONFLICT (document_hash) DO NOTHING
                        """.format(schema), (
                            doc["content"],
                            doc["embedding"],
                            doc["document_hash"],
                            doc["version"],
                            doc["processed_at"],
                            doc["source"],
                            json.dumps(doc["metadata"])
                        ))
                        if cur.rowcount > 0:
                            inserted_count += 1
                    except Exception as e:
                        print(f"Error inserting embedding: {str(e)}")
            conn.commit()
        return inserted_count