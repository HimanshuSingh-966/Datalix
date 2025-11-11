from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, List, Any, Dict
import uvicorn
import os
from dotenv import load_dotenv

from auth import get_current_user, router as auth_router
from data_processor import DataProcessor
from ai_service import AIService
from example_data import get_example_dataset, list_example_datasets

load_dotenv()

app = FastAPI(title="DataLix 2.0 API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances - shared data processor for session consistency
data_processor = DataProcessor()
ai_service = AIService(data_processor)

# Include auth routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# Request/Response Models
class ChatRequest(BaseModel):
    session_id: str
    message: str
    provider: Optional[str] = "auto"

class ChatResponse(BaseModel):
    message: str
    function_calls: Optional[List[str]] = None
    results: Optional[Any] = None
    data_preview: Optional[Dict] = None
    chart_data: Optional[Dict] = None
    suggested_actions: Optional[List[Dict]] = None
    quality_score: Optional[float] = None

class OperationRequest(BaseModel):
    session_id: str
    operation: str
    parameters: Optional[Dict] = None

@app.get("/")
async def root():
    return {"message": "DataLix 2.0 API", "version": "2.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "python_version": "3.11"}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user: Dict = Depends(get_current_user)
):
    """Upload and analyze a dataset"""
    try:
        # Read file content
        content = await file.read()
        
        # Get filename, default to 'unknown.csv' if None
        filename = file.filename or 'unknown.csv'
        
        # Process the file
        session_id, result = await data_processor.process_upload(
            content, filename, user['id']
        )
        
        return {
            "sessionId": session_id,
            "datasetInfo": result["dataset_info"],
            "qualityScore": result["quality_score"],
            "preview": result["preview"],
            "issues": result["issues"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: Dict = Depends(get_current_user)
):
    """Process natural language queries using AI (Groq or Gemini)"""
    try:
        provider = request.provider or "auto"
        response = await ai_service.process_message(
            session_id=request.session_id,
            message=request.message,
            user_id=user['id'],
            provider=provider
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/ai-providers")
async def get_ai_providers():
    """Get available AI providers"""
    return {
        "providers": {
            "gemini": ai_service.gemini_available,
            "groq": ai_service.groq_available
        },
        "default": "groq" if ai_service.groq_available else "gemini" if ai_service.gemini_available else None
    }

@app.post("/statistics")
async def get_statistics(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Get statistical summary of dataset"""
    try:
        stats = data_processor.calculate_statistics(request.session_id)
        return {"statistics": stats}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/correlation")
async def get_correlation(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Get correlation matrix"""
    try:
        corr = data_processor.calculate_correlation(request.session_id)
        return {"correlation": corr}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/visualize")
async def create_visualization(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Create a visualization"""
    try:
        params = request.parameters or {}
        chart = data_processor.create_visualization(
            session_id=request.session_id,
            chart_type=params.get('chart_type', 'scatter'),
            x_column=params.get('x_column', ''),
            y_column=params.get('y_column', ''),
            parameters=params
        )
        return {"chartData": chart}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/clean")
async def clean_data(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Clean dataset (handle missing values, outliers, duplicates)"""
    try:
        params = request.parameters or {}
        result = data_processor.clean_data(
            session_id=request.session_id,
            parameters=params
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ml-analysis")
async def ml_analysis(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Perform ML analysis (clustering, anomaly detection, etc.)"""
    try:
        params = request.parameters or {}
        result = data_processor.ml_analysis(
            session_id=request.session_id,
            analysis_type=params.get('analysis_type', 'clustering'),
            parameters=params
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/export")
async def export_data(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Export dataset in various formats"""
    try:
        params = request.parameters or {}
        file_path = data_processor.export_data(
            session_id=request.session_id,
            format=params.get('format', 'csv'),
            parameters=params
        )
        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            filename=os.path.basename(file_path)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sessions")
async def get_sessions(user: Dict = Depends(get_current_user)):
    """Get user's data sessions"""
    try:
        sessions = data_processor.get_user_sessions(user['id'])
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    user: Dict = Depends(get_current_user)
):
    """Delete a data session"""
    try:
        data_processor.delete_session(session_id)
        return {"message": "Session deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/example-datasets")
async def get_example_datasets():
    """List available example datasets"""
    return {"datasets": list_example_datasets()}

@app.post("/load-example-dataset")
async def load_example_dataset(
    dataset_id: str,
    user: Dict = Depends(get_current_user)
):
    """Load an example dataset"""
    try:
        csv_data = get_example_dataset(dataset_id)
        
        datasets = list_example_datasets()
        dataset_info = next((d for d in datasets if d['id'] == dataset_id), None)
        if not dataset_info:
            raise HTTPException(status_code=404, detail="Dataset not found")
        
        filename = f"{dataset_id}_example.csv"
        
        session_id, result = await data_processor.process_upload(
            csv_data, filename, user['id']
        )
        
        return {
            "sessionId": session_id,
            "datasetInfo": result["dataset_info"],
            "qualityScore": result["quality_score"],
            "preview": result["preview"],
            "issues": result["issues"],
            "exampleDatasetName": dataset_info['name']
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
