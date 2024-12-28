# src/processors/__init__.py
from .docx_processor import DocxProcessor
from .txt_processor import TextProcessor
from .pdf_processor import PDFProcessor
from .py_processor import PythonProcessor
from .registry import ProcessorRegistry

# Register processors
ProcessorRegistry.register_processor(DocxProcessor)
ProcessorRegistry.register_processor(TextProcessor)
ProcessorRegistry.register_processor(PDFProcessor)
ProcessorRegistry.register_processor(PythonProcessor)
