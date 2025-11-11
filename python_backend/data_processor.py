import pandas as pd
import numpy as np
import json
import io
import uuid
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

from data_quality import analyze_data_quality
from statistics_module import calculate_statistics, calculate_correlation
from ml_analysis import perform_ml_analysis
from visualizations import create_visualization as create_viz
from data_cleaning import clean_dataset, handle_missing_values, detect_and_handle_outliers, remove_duplicates

class DataProcessor:
    def __init__(self):
        # In-memory storage for datasets
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    async def process_upload(
        self, 
        content: bytes, 
        filename: str, 
        user_id: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Process uploaded file and create a new session"""
        
        # Parse file based on extension
        ext = filename.lower().split('.')[-1]
        
        try:
            if ext == 'csv':
                df = pd.read_csv(io.BytesIO(content))
            elif ext in ['xlsx', 'xls']:
                df = pd.read_excel(io.BytesIO(content))
            elif ext == 'json':
                df = pd.read_json(io.BytesIO(content))
            elif ext == 'parquet':
                df = pd.read_parquet(io.BytesIO(content))
            else:
                raise ValueError(f"Unsupported file format: {ext}")
        except Exception as e:
            raise ValueError(f"Failed to parse file: {str(e)}")
        
        # Create session
        session_id = str(uuid.uuid4())
        
        # Analyze data quality
        quality_analysis = analyze_data_quality(df)
        
        # Create preview
        preview = self._create_preview(df, filename)
        
        # Store session
        self.sessions[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "dataframe": df,
            "filename": filename,
            "created_at": datetime.now(),
            "quality": quality_analysis,
            "preview": preview
        }
        
        # Prepare response
        result = {
            "dataset_info": {
                "rows": len(df),
                "columns": len(df.columns),
                "sizeMb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
                "columnNames": df.columns.tolist(),
                "columnTypes": df.dtypes.astype(str).to_dict()
            },
            "quality_score": quality_analysis["overallScore"],
            "preview": preview,
            "issues": quality_analysis["issues"]
        }
        
        return session_id, result
    
    def _create_preview(self, df: pd.DataFrame, filename: str = None, max_rows: int = 100) -> Dict:
        """Create a data preview"""
        preview_df = df.head(max_rows)
        
        columns_info = []
        for col in df.columns:
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()
            sample_values = df[col].dropna().unique()[:5].tolist()
            
            columns_info.append({
                "name": col,
                "type": str(df[col].dtype),
                "nullCount": int(null_count),
                "uniqueCount": int(unique_count),
                "sampleValues": sample_values
            })
        
        # Convert DataFrame to records, handling NaN values
        rows = preview_df.replace({np.nan: None}).to_dict('records')
        
        return {
            "columns": columns_info,
            "rows": rows,
            "totalRows": len(df),
            "totalColumns": len(df.columns),
            "fileName": filename
        }
    
    def get_dataframe(self, session_id: str) -> pd.DataFrame:
        """Get DataFrame for a session"""
        if session_id not in self.sessions:
            raise ValueError("Session not found")
        return self.sessions[session_id]["dataframe"]
    
    def update_dataframe(self, session_id: str, df: pd.DataFrame):
        """Update DataFrame for a session"""
        if session_id not in self.sessions:
            raise ValueError("Session not found")
        
        self.sessions[session_id]["dataframe"] = df
        self.sessions[session_id]["preview"] = self._create_preview(df, self.sessions[session_id].get("filename"))
        
        # Recalculate quality
        quality = analyze_data_quality(df)
        self.sessions[session_id]["quality"] = quality
    
    def calculate_statistics(self, session_id: str, columns: Optional[List[str]] = None) -> Dict:
        """Calculate statistical summary"""
        df = self.get_dataframe(session_id)
        return calculate_statistics(df, columns)
    
    def calculate_correlation(self, session_id: str, columns: Optional[List[str]] = None) -> Dict:
        """Calculate correlation matrix"""
        df = self.get_dataframe(session_id)
        return calculate_correlation(df, columns)
    
    def detect_missing_values(self, session_id: str) -> Dict:
        """Detect and return columns with missing values"""
        df = self.get_dataframe(session_id)
        
        missing_info = []
        total_rows = len(df)
        
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            if missing_count > 0:
                missing_percentage = (missing_count / total_rows) * 100
                missing_info.append({
                    "column": col,
                    "missing_count": int(missing_count),
                    "missing_percentage": round(missing_percentage, 2),
                    "data_type": str(df[col].dtype)
                })
        
        return {
            "total_rows": total_rows,
            "columns_with_missing": len(missing_info),
            "missing_data": missing_info
        }
    
    def create_visualization(
        self,
        session_id: str,
        chart_type: str,
        x_column: Optional[str] = None,
        y_column: Optional[str] = None,
        parameters: Optional[Dict] = None
    ) -> Dict:
        """Create a Plotly visualization"""
        df = self.get_dataframe(session_id)
        return create_viz(df, chart_type, x_column, y_column, parameters or {})
    
    def clean_data(self, session_id: str, parameters: Dict) -> Dict:
        """Clean dataset"""
        df = self.get_dataframe(session_id)
        result = clean_dataset(df, parameters)
        
        # Update the dataframe
        self.update_dataframe(session_id, result["dataframe"])
        
        return {
            "message": result["message"],
            "changes": result["changes"],
            "preview": self.sessions[session_id]["preview"],
            "quality": self.sessions[session_id]["quality"]
        }
    
    def ml_analysis(
        self,
        session_id: str,
        analysis_type: str,
        parameters: Optional[Dict] = None
    ) -> Dict:
        """Perform ML analysis"""
        df = self.get_dataframe(session_id)
        return perform_ml_analysis(df, analysis_type, parameters or {})
    
    def export_data(
        self,
        session_id: str,
        format: str = 'csv',
        parameters: Optional[Dict] = None
    ) -> str:
        """Export dataset to file"""
        df = self.get_dataframe(session_id)
        params = parameters or {}
        
        # Create export directory
        import os
        os.makedirs('/tmp/exports', exist_ok=True)
        
        filename = params.get('filename', f'export_{session_id[:8]}')
        
        if format == 'csv':
            filepath = f'/tmp/exports/{filename}.csv'
            df.to_csv(filepath, index=False, encoding=params.get('encoding', 'utf-8'))
        elif format == 'excel':
            filepath = f'/tmp/exports/{filename}.xlsx'
            df.to_excel(filepath, index=False)
        elif format == 'json':
            filepath = f'/tmp/exports/{filename}.json'
            df.to_json(filepath, orient='records', indent=2)
        elif format == 'parquet':
            filepath = f'/tmp/exports/{filename}.parquet'
            df.to_parquet(filepath, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        return filepath
    
    def get_user_sessions(self, user_id: str) -> List[Dict]:
        """Get all sessions for a user"""
        sessions = []
        for session_id, session in self.sessions.items():
            if session["user_id"] == user_id:
                sessions.append({
                    "sessionId": session_id,
                    "filename": session.get("filename"),
                    "createdAt": session["created_at"].isoformat(),
                    "rows": len(session["dataframe"]),
                    "columns": len(session["dataframe"].columns),
                    "qualityScore": session["quality"]["overallScore"]
                })
        return sessions
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
