from typing import Dict, Any, List, Optional
import PyPDF2
from .base_processor import BaseProcessor
from .registry import ProcessorRegistry
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

@ProcessorRegistry.register
class PDFProcessor(BaseProcessor):
    PROCESS_TYPES = {
        'default': {'chunk_size': 1000, 'chunk_overlap': 200},
        'fine': {'chunk_size': 500, 'chunk_overlap': 100},
        'coarse': {'chunk_size': 2000, 'chunk_overlap': 400},
        'page': {'chunk_size': None, 'chunk_overlap': 0},  # Process page by page
        'section': {'chunk_size': None, 'chunk_overlap': 50}  # Process by PDF sections/bookmarks
    }

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.supported_extensions = {'.pdf'}
        self.configure_splitter(chunk_size, chunk_overlap)

    def configure_splitter(self, chunk_size: Optional[int], chunk_overlap: int):
        if chunk_size:
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                separators=["\n\n", "\n", " ", ""]
            )
        else:
            self.text_splitter = None

    def process(self, file_path: str, process_type: Optional[str] = None) -> List[Dict[str, Any]]:
        if process_type and process_type not in self.get_supported_process_types():
            raise ValueError(f"Unsupported process type: {process_type}")

        if process_type:
            config = self.PROCESS_TYPES[process_type]
            self.configure_splitter(config['chunk_size'], config['chunk_overlap'])

        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            metadata = self.get_metadata(file_path)

            if process_type == 'page':
                return self._process_by_pages(pdf_reader, metadata)
            elif process_type == 'section':
                return self._process_by_sections(pdf_reader, metadata)
            else:
                return self._process_with_chunking(pdf_reader, metadata)

    @classmethod
    def get_supported_process_types(cls) -> set:
        return set(cls.PROCESS_TYPES.keys())

    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            info = pdf_reader.metadata
            return {
                'file_type': 'pdf',
                'file_name': os.path.basename(file_path),
                'file_size': os.path.getsize(file_path),
                'num_pages': len(pdf_reader.pages),
                'author': info.get('/Author', None),
                'creator': info.get('/Creator', None),
                'producer': info.get('/Producer', None),
                'subject': info.get('/Subject', None),
                'title': info.get('/Title', None),
                'creation_date': info.get('/CreationDate', None)
            } 