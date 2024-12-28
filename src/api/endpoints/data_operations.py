from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import List, Optional
from services.data_processor import DataProcessorService
from core.config import settings
from processors.processor_registry import ProcessorRegistry

router = APIRouter()
data_processor = DataProcessorService()

@router.post("/upload/{source_type}")
async def upload_data(
    source_type: str,
    files: List[UploadFile] = File(...),
    process_type: Optional[str] = Query(None, description="Specific processing type")
):
    """
    Upload and process data from various sources
    
    Args:
        source_type: Type of data source (csv, json, xml, etc.)
        files: List of files to process
        process_type: Optional specific processing type
    """
    # Validate source_type is supported
    supported_types = {ext.lstrip('.') for processor in ProcessorRegistry._processors.values() 
                      for ext in processor.get_supported_extensions()}
    if source_type.lower() not in supported_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported source type. Supported types: {', '.join(supported_types)}"
        )
    
    try:
        results = await data_processor.process_files(
            files=files,
            source_type=source_type,
            process_type=process_type
        )
        return {"status": "success", "results": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))