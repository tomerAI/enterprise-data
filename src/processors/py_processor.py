from typing import Dict, Any, List, set, Optional
from .base_processor import BaseProcessor
import ast
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from datetime import datetime

class PythonProcessor(BaseProcessor):
    PROCESS_TYPES = {
        'default': {'chunk_size': 1000, 'chunk_overlap': 200},
        'fine': {'chunk_size': 500, 'chunk_overlap': 100},
        'coarse': {'chunk_size': 2000, 'chunk_overlap': 400},
        'function': {'chunk_size': None, 'chunk_overlap': 0},  # Process function by function
        'class': {'chunk_size': None, 'chunk_overlap': 0}  # Process class by class
    }

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.supported_extensions = {'.py'}
        self.configure_splitter(chunk_size, chunk_overlap)

    def configure_splitter(self, chunk_size: int, chunk_overlap: int):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\nclass ", "\ndef ", "\n\n", "\n", " ", ""]
        )
        
    @classmethod
    def get_supported_extensions(cls) -> set:
        return {'.py'}
    
    def process(self, file_path: str, process_type: Optional[str] = None) -> List[Dict[str, Any]]:
        if process_type and process_type not in self.get_supported_process_types():
            raise ValueError(f"Unsupported process type: {process_type}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        tree = ast.parse(content)
        metadata = self._extract_metadata(content, file_path)

        if process_type == 'function':
            return self._process_by_functions(tree, metadata)
        elif process_type == 'class':
            return self._process_by_classes(tree, metadata)
        else:
            return self._process_with_chunking(content, metadata)
    
    def _extract_metadata(self, content: str, file_path: str) -> Dict[str, Any]:
        """Extract comprehensive metadata from Python file using AST"""
        try:
            tree = ast.parse(content)
            
            # Extract imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(n.name for n in node.names)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    imports.extend(f"{module}.{n.name}" for n in node.names)
            
            # Extract classes with their methods
            classes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = []
                    for child in ast.iter_child_nodes(node):
                        if isinstance(child, ast.FunctionDef):
                            methods.append({
                                "name": child.name,
                                "args": len(child.args.args),
                                "decorators": [
                                    ast.unparse(d) for d in child.decorator_list
                                ] if hasattr(ast, 'unparse') else []
                            })
                    classes.append({
                        "name": node.name,
                        "methods": methods,
                        "decorators": [
                            ast.unparse(d) for d in node.decorator_list
                        ] if hasattr(ast, 'unparse') else []
                    })
            
            # Extract top-level functions
            functions = []
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "args": len(node.args.args),
                        "decorators": [
                            ast.unparse(d) for d in node.decorator_list
                        ] if hasattr(ast, 'unparse') else []
                    })
            
            return {
                "type": "python",
                "source": file_path,
                "filename": os.path.basename(file_path),
                "file_size": os.path.getsize(file_path),
                "created_at": datetime.now().isoformat(),
                "code_stats": {
                    "classes": len(classes),
                    "functions": len(functions),
                    "imports": len(imports),
                    "lines": len(content.splitlines())
                },
                "code_structure": {
                    "imports": imports,
                    "classes": classes,
                    "functions": functions
                }
            }
            
        except SyntaxError as e:
            return {
                "type": "python",
                "source": file_path,
                "filename": os.path.basename(file_path),
                "file_size": os.path.getsize(file_path),
                "created_at": datetime.now().isoformat(),
                "parse_error": f"Syntax error at line {e.lineno}: {str(e)}"
            }
        except Exception as e:
            return {
                "type": "python",
                "source": file_path,
                "filename": os.path.basename(file_path),
                "file_size": os.path.getsize(file_path),
                "created_at": datetime.now().isoformat(),
                "parse_error": str(e)
            } 

    @classmethod
    def get_supported_process_types(cls) -> set:
        return set(cls.PROCESS_TYPES.keys()) 