from fastapi import APIRouter
from .endpoints import data_operations, retrieval

# Main API Router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(
    data_operations.router,
    prefix="/data",
    tags=["data-operations"]
)

api_router.include_router(
    retrieval.router,
    prefix="/retrieve",
    tags=["retrieval"]
) 