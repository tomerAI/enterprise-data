from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.retrieval_service import RetrievalService

router = APIRouter()
retrieval_service = RetrievalService()

@router.get("/search")
async def search(
    query: str,
    max_results: Optional[int] = Query(default=5, gt=0, le=20),
    graph_depth: Optional[int] = Query(default=2, ge=1, le=5)
):
    """
    Search across documents using semantic search enhanced with graph relationships.
    
    Parameters:
    - query: Search query string
    - max_results: Maximum number of results to return (default: 5)
    - graph_depth: Depth of graph traversal for related nodes (default: 2)
    """
    try:
        results = await retrieval_service.graph_enhanced_search(
            query=query,
            max_results=max_results,
            depth=graph_depth
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 