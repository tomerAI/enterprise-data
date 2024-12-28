from typing import List, Dict, Any, Optional
from fastapi import UploadFile
import os
from .embedding_service import EmbeddingService
from processors.registry import ProcessorRegistry

class DataProcessorService:
    def __init__(self):
        self.embedding_service = EmbeddingService()

    async def process_files(
        self,
        files: List[UploadFile],
        source_type: str,
        process_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Process uploaded files based on their source type and optional process type"""
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
                
                # Validate process_type if provided
                if process_type and process_type not in processor.get_supported_process_types():
                    raise ValueError(
                        f"Unsupported process type '{process_type}' for {file_ext} files. "
                        f"Supported types: {', '.join(processor.get_supported_process_types())}"
                    )
                
                processed_data = processor.process(temp_path, process_type=process_type)

                # Generate embeddings and store in vector DB
                embedding_count = self.embedding_service.process_and_store_file(temp_path)

                results.append({
                    "filename": file.filename,
                    "embeddings_stored": embedding_count
                })

            finally:
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        return results 