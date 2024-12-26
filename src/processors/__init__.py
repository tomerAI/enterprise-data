# src/processors/__init__.py
from .graph_csv_processor import GraphCSVProcessor
from .registry import ProcessorRegistry

# Register Graph CSV Processor
ProcessorRegistry.register_processor(GraphCSVProcessor)
