from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from services.retrieval_service import RetrievalService

router = APIRouter()
retrieval_service = RetrievalService()

@router.get("/search")
async def search(
    query: str,
    max_results: Optional[int] = Query(default=5, gt=0, le=20),
    similarity_threshold: Optional[float] = Query(default=0.7, gt=0, le=1.0)
):
    """
    Search across documents using semantic search with RAG.
    
    Parameters:
    - query: Search query string
    - max_results: Maximum number of results to return (default: 5)
    - similarity_threshold: Minimum similarity score threshold (default: 0.7)
    """
    try:
        results = await retrieval_service.semantic_search(
            query=query,
            limit=max_results,
            threshold=similarity_threshold
        )
        return {
            "query": query,
            "results": results,
            "result_count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 