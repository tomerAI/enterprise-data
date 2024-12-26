from typing import List, Dict, Any
from fastapi import UploadFile
import os
from .embedding_service import EmbeddingService
from .graph_service import GraphService
from processors.registry import ProcessorRegistry

class DataProcessorService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.graph_service = GraphService()

    async def process_files(
        self,
        files: List[UploadFile],
        source_type: str,
        process_type: str = None
    ) -> List[Dict[str, Any]]:
        """
        Process uploaded files based on their source type and optional process type
        """
        results = []
        
        for file in files:
            # Validate file extension matches source_type
            file_ext = os.path.splitext(file.filename)[1].lower()
            if not file_ext.lstrip('.') == source_type.lower():
                raise ValueError(f"File {file.filename} does not match source type {source_type}")

            # Save file temporarily
            temp_path = f"/tmp/{file.filename}"
            with open(temp_path, "wb") as f:
                content = await file.read()
                f.write(content)

            try:
                # Process file based on source type
                processor = ProcessorRegistry.get_processor(file_ext)()
                processed_data = processor.process(temp_path)

                # Generate embeddings and store in vector DB
                embedding_count = self.embedding_service.process_and_store_file(temp_path)

                # If it's a graph-compatible format, store in graph DB
                graph_count = 0
                if hasattr(processor, 'process_graph'):
                    graph_elements = processor.process_graph(temp_path)
                    graph_count = self.graph_service.create_graph_elements(graph_elements)

                results.append({
                    "filename": file.filename,
                    "embeddings_stored": embedding_count,
                    "graph_elements_created": graph_count
                })

            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        return results

    async def query_graph(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a graph query"""
        return self.graph_service.query_graph(
            query=query.get('cypher'),
            params=query.get('params', {})
        ) 