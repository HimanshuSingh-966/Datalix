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
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

# Request/Response Models
class ChatRequest(BaseModel):
    session_id: str
    message: str

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

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "python_version": "3.11"}

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    user: Dict = Depends(get_current_user)
):
    """Upload and analyze a dataset"""
    try:
        # Read file content
        content = await file.read()
        
        # Process the file
        session_id, result = await data_processor.process_upload(
            content, file.filename, user['id']
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

@app.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: Dict = Depends(get_current_user)
):
    """Process natural language queries using Gemini AI"""
    try:
        response = await ai_service.process_message(
            session_id=request.session_id,
            message=request.message,
            user_id=user['id']
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/statistics")
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

@app.post("/api/correlation")
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

@app.post("/api/visualize")
async def create_visualization(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Create a visualization"""
    try:
        chart = data_processor.create_visualization(
            session_id=request.session_id,
            chart_type=request.parameters.get('chart_type'),
            x_column=request.parameters.get('x_column'),
            y_column=request.parameters.get('y_column'),
            parameters=request.parameters
        )
        return {"chartData": chart}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/clean")
async def clean_data(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Clean dataset (handle missing values, outliers, duplicates)"""
    try:
        result = data_processor.clean_data(
            session_id=request.session_id,
            parameters=request.parameters
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/ml-analysis")
async def ml_analysis(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Perform ML analysis (clustering, anomaly detection, etc.)"""
    try:
        result = data_processor.ml_analysis(
            session_id=request.session_id,
            analysis_type=request.parameters.get('analysis_type'),
            parameters=request.parameters
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/export")
async def export_data(
    request: OperationRequest,
    user: Dict = Depends(get_current_user)
):
    """Export dataset in various formats"""
    try:
        file_path = data_processor.export_data(
            session_id=request.session_id,
            format=request.parameters.get('format', 'csv'),
            parameters=request.parameters
        )
        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            filename=os.path.basename(file_path)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/sessions")
async def get_sessions(user: Dict = Depends(get_current_user)):
    """Get user's data sessions"""
    try:
        sessions = data_processor.get_user_sessions(user['id'])
        return {"sessions": sessions}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/sessions/{session_id}")
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

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
