from typing import Dict, Any, List, set, Optional
from .base_processor import BaseProcessor
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from datetime import datetime

class TextProcessor(BaseProcessor):
    PROCESS_TYPES = {
        'default': {'chunk_size': 1000, 'chunk_overlap': 200},
        'fine': {'chunk_size': 500, 'chunk_overlap': 100},
        'coarse': {'chunk_size': 2000, 'chunk_overlap': 400},
        'line': {'chunk_size': None, 'chunk_overlap': 0},  # Process line by line
        'paragraph': {'chunk_size': None, 'chunk_overlap': 0}  # Process paragraph by paragraph
    }

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.supported_extensions = {'.txt'}
        self.configure_splitter(chunk_size, chunk_overlap)

    def configure_splitter(self, chunk_size: int, chunk_overlap: int):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    @classmethod
    def get_supported_extensions(cls) -> set:
        return {'.txt'}
    
    def process(self, file_path: str, process_type: Optional[str] = None) -> List[Dict[str, Any]]:
        if process_type and process_type not in self.get_supported_process_types():
            raise ValueError(f"Unsupported process type: {process_type}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        metadata = self._extract_metadata(file_path)

        if process_type == 'line':
            return self._process_by_lines(content, metadata)
        elif process_type == 'paragraph':
            return self._process_by_paragraphs(content, metadata)
        else:
            return self._process_with_chunking(content, metadata)

    @classmethod
    def get_supported_process_types(cls) -> set:
        return set(cls.PROCESS_TYPES.keys())
    
    def _extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from the text file"""
        return {
            "type": "text",
            "source": file_path,
            "filename": os.path.basename(file_path),
            "file_size": os.path.getsize(file_path),
            "created_at": datetime.now().isoformat(),
            "document_stats": {
                "size_bytes": os.path.getsize(file_path),
                "last_modified": datetime.fromtimestamp(
                    os.path.getmtime(file_path)
                ).isoformat()
            }
        } 