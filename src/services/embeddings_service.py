# src/services/embedding_service.py
import os
import hashlib
import json
from datetime import datetime
import psycopg2

from langchain.embeddings import OpenAIEmbeddings

from processors.registry import ProcessorRegistry
from utils.db import get_db_params, wait_for_db

class EmbeddingService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.db_params = get_db_params()

        # Ensure DB is ready
        if not wait_for_db(self.db_params):
            raise RuntimeError("Database connection failed")

    def _generate_document_hash(self, content: str) -> str:
        return hashlib.md5(content.encode()).hexdigest()

    def process_and_store_file(self, file_path: str) -> int:
        """Process a single file (CSV, etc.) and store embeddings in DB. Returns count of records inserted."""
        file_ext = os.path.splitext(file_path)[1].lower()
        processor_class = ProcessorRegistry.get_processor(file_ext)
        processor = processor_class()

        # 1) Split document into chunks
        chunks = processor.process(file_path)

        # 2) Generate embeddings for each chunk
        embedded_documents = []
        for chunk in chunks:
            content = chunk["content"]
            metadata = chunk["metadata"]
            doc_hash = self._generate_document_hash(content)
            vector = self.embeddings.embed_query(content)

            embedded_documents.append({
                "content": content,
                "embedding": vector,
                "document_hash": doc_hash,
                "metadata": metadata,
                "source": file_path,
                "version": "1.0",
                "processed_at": datetime.now().isoformat()
            })

        # 3) Insert into Postgres
        return self.store_embeddings(embedded_documents)

    def store_embeddings(self, embedded_documents) -> int:
        """Store each embedded document in the Postgres embeddings table. Returns the count of inserted rows."""
        schema = os.getenv("DBT_SCHEMA", "permanent")
        inserted_count = 0

        with psycopg2.connect(**self.db_params) as conn:
            with conn.cursor() as cur:
                for emb in embedded_documents:
                    try:
                        cur.execute(f"""
                            INSERT INTO {schema}.embeddings 
                            (content, embedding, document_hash, version, processed_at, source, metadata)
                            VALUES (%s, %s::vector, %s, %s, %s, %s, %s)
                            ON CONFLICT (document_hash) DO NOTHING
                        """, (
                            emb["content"],
                            emb["embedding"],
                            emb["document_hash"],
                            emb["version"],
                            emb["processed_at"],
                            emb["source"],
                            json.dumps(emb.get("metadata", {}))
                        ))
                        # If row inserted (no conflict)
                        if cur.rowcount > 0:
                            inserted_count += 1
                    except Exception as e:
                        print(f"Error inserting embeddings: {str(e)}")
                        # Optionally continue or raise error
            conn.commit()

        return inserted_count
