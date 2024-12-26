# src/processors/registry.py
from typing import Type, Dict
from .base_processor import BaseProcessor

class ProcessorRegistry:
    _processors: Dict[str, Type[BaseProcessor]] = {}

    @classmethod
    def register_processor(cls, processor_class: Type[BaseProcessor]):
        """Register a processor for specific file extensions"""
        for ext in processor_class.get_supported_extensions():
            cls._processors[ext.lower()] = processor_class

    @classmethod
    def get_processor(cls, file_extension: str) -> Type[BaseProcessor]:
        """Get appropriate processor for file extension"""
        ext = file_extension.lower()
        if ext.startswith('.'):
            ext = ext[1:]
        processor_class = cls._processors.get(ext)
        if not processor_class:
            raise ValueError(f"No processor found for extension: {file_extension}")
        return processor_class
