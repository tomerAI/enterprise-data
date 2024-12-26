from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseProcessor(ABC):
    @abstractmethod
    def process(self, file_path: str) -> List[Dict[str, Any]]:
        """Process a file and return a list of document chunks"""
        pass

    @classmethod
    @abstractmethod
    def get_supported_extensions(cls) -> set:
        """Return a set of supported file extensions"""
        pass 