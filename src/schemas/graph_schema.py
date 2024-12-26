from enum import Enum
from typing import Dict, Any

class NodeType(str, Enum):
    DOCUMENT = "Document"
    ENTITY = "Entity"
    CONCEPT = "Concept"
    SECTION = "Section"

class RelationType(str, Enum):
    CONTAINS = "CONTAINS"
    RELATES_TO = "RELATES_TO"
    REFERENCES = "REFERENCES"
    SIMILAR_TO = "SIMILAR_TO"

class GraphSchema:
    @staticmethod
    def create_document_node(content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "label": NodeType.DOCUMENT,
            "properties": {
                "content": content,
                "type": metadata.get("type", "unknown"),
                "created_at": metadata.get("created_at"),
                "source": metadata.get("source")
            }
        }
