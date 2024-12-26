# src/main.py
import uvicorn
from fastapi import FastAPI
from api.router import api_router
from core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Enterprise Graph RAG API",
        version=settings.VERSION
    )
    
    # Include main API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
