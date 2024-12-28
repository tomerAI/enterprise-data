from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseProcessor(ABC):
    @abstractmethod
    def process(self, file_path: str, process_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Process a file and return a list of document chunks
        
        Args:
            file_path: Path to the file to process
            process_type: Optional processing strategy to use
        """
        pass

    @classmethod
    @abstractmethod
    def get_supported_extensions(cls) -> set:
        """Return a set of supported file extensions"""
        pass
    
    @classmethod
    @abstractmethod
    def get_supported_process_types(cls) -> set:
        """Return a set of supported processing types"""
        pass 