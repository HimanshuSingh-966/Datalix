import os
import json
from typing import Dict, Any, List, Optional
import google.generativeai as genai
import google.ai.generativelanguage as glm
from groq import Groq
from data_processor import DataProcessor
from statistics_module import calculate_statistics, calculate_correlation
from visualizations import create_visualization
from data_cleaning import clean_dataset, handle_missing_values
from ml_analysis import perform_ml_analysis

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✓ Gemini AI configured")
else:
    print("⚠️  Warning: GEMINI_API_KEY not set.")

# Configure Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
    print("✓ Groq AI configured")
else:
    groq_client = None
    print("⚠️  Warning: GROQ_API_KEY not set.")

# At least one provider must be configured
if not GEMINI_API_KEY and not GROQ_API_KEY:
    print("❌ ERROR: No AI provider configured. Set GEMINI_API_KEY or GROQ_API_KEY.")

class AIService:
    def __init__(self, data_processor: DataProcessor):
        """Initialize AI service with shared data processor instance."""
        self.data_processor = data_processor
        self.gemini_available = bool(GEMINI_API_KEY)
        self.groq_available = bool(GROQ_API_KEY)
        
        # Initialize Gemini model with function calling using proper glm format
        if GEMINI_API_KEY:
            # Define function declarations using glm for type-safe declarations
            tool = glm.Tool(
                function_declarations=[
                    glm.FunctionDeclaration(
                        name="get_statistics",
                        description="Calculate statistical summary (mean, median, std, min, max, quartiles) for numeric columns",
                        parameters=glm.Schema(
                            type=glm.Type.OBJECT,
                            properties={
                                "columns": glm.Schema(
                                    type=glm.Type.STRING,
                                    description="Comma-separated column names to analyze"
                                )
                            }
                        )
                    ),
                    glm.FunctionDeclaration(
                        name="detect_missing_values",
                        description="Show all columns that have missing/null values with counts and percentages",
                        parameters=glm.Schema(
                            type=glm.Type.OBJECT,
                            properties={}
                        )
                    ),
                    glm.FunctionDeclaration(
                        name="create_visualization",
                        description="Create charts: histogram, scatter, line, bar, box, violin, heatmap, correlation, pie",
                        parameters=glm.Schema(
                            type=glm.Type.OBJECT,
                            properties={
                                "chart_type": glm.Schema(
                                    type=glm.Type.STRING,
                                    description="Type: histogram, scatter, line, bar, heatmap, correlation, pie"
                                ),
                                "x_column": glm.Schema(
                                    type=glm.Type.STRING,
                                    description="Column for X-axis"
                                ),
                                "y_column": glm.Schema(
                                    type=glm.Type.STRING,
                                    description="Column for Y-axis"
                                ),
                                "title": glm.Schema(
                                    type=glm.Type.STRING,
                                    description="Chart title"
                                )
                            },
                            required=["chart_type"]
                        )
                    ),
                    glm.FunctionDeclaration(
                        name="clean_data",
                        description="Clean dataset: handle missing values, outliers, duplicates",
                        parameters=glm.Schema(
                            type=glm.Type.OBJECT,
                            properties={
                                "action": glm.Schema(
                                    type=glm.Type.STRING,
                                    description="Action: handle_missing, remove_outliers, remove_duplicates"
                                ),
                                "method": glm.Schema(
                                    type=glm.Type.STRING,
                                    description="Method: mean, median, drop, iqr, zscore"
                                )
                            },
                            required=["action"]
                        )
                    ),
                    glm.FunctionDeclaration(
                        name="show_data_preview",
                        description="Display the current dataset table to show the user the data",
                        parameters=glm.Schema(
                            type=glm.Type.OBJECT,
                            properties={}
                        )
                    )
                ]
            )
            
            self.model = genai.GenerativeModel(
                'gemini-1.5-flash',
                tools=[tool]
            )
        else:
            self.model = None
    
    async def process_message(
        self,
        session_id: str,
        message: str,
        user_id: str,
        provider: str = "auto"
    ) -> Dict[str, Any]:
        """Process user message using AI (Gemini or Groq) with function calling
        
        Args:
            session_id: The data session ID
            message: User's message
            user_id: User ID
            provider: 'gemini', 'groq', or 'auto' (auto selects best available)
        """
        
        # Determine which provider to use
        if provider == "auto":
            if self.groq_available:
                provider = "groq"
            elif self.gemini_available:
                provider = "gemini"
            else:
                return {
                    "message": "⚠️ No AI provider configured. Please set GEMINI_API_KEY or GROQ_API_KEY.",
                    "function_calls": None,
                    "results": None
                }
        
        # Route to appropriate provider
        if provider == "groq" and self.groq_available:
            return await self._process_with_groq(session_id, message, user_id)
        elif provider == "gemini" and self.gemini_available:
            return await self._process_with_gemini(session_id, message, user_id)
        else:
            return {
                "message": f"⚠️ {provider.capitalize()} is not available. Please configure the API key.",
                "function_calls": None,
                "results": None
            }
    
    async def _process_with_gemini(
        self,
        session_id: str,
        message: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Process user message using Gemini AI with function calling"""
        
        if not self.model:
            return {
                "message": "⚠️ Gemini not configured.",
                "function_calls": None,
                "results": None
            }
        
        # Get dataset info for context
        try:
            df = self.data_processor.get_dataframe(session_id)
            
            # Get missing value info
            missing_info = []
            for col in df.columns:
                missing_count = df[col].isnull().sum()
                if missing_count > 0:
                    missing_pct = (missing_count / len(df)) * 100
                    missing_info.append(f"{col}: {missing_count} ({missing_pct:.1f}%)")
            
            # Get numeric column stats preview
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            stats_preview = []
            for col in numeric_cols[:5]:
                stats_preview.append(f"{col}: min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}")
            
            dataset_context = f"""
You are analyzing a dataset with the following ACTUAL data:

DATASET OVERVIEW:
- Total rows: {len(df)}
- Total columns: {len(df.columns)}
- File size: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB

COLUMNS ({len(df.columns)} total):
{chr(10).join([f"- {col} ({df[col].dtype}): {df[col].nunique()} unique values" for col in df.columns])}

MISSING VALUES:
{chr(10).join([f"- {info}" for info in missing_info]) if missing_info else "- No missing values found"}

NUMERIC COLUMNS PREVIEW:
{chr(10).join([f"- {stat}" for stat in stats_preview]) if stats_preview else "- No numeric columns"}

DATA PREVIEW (first 3 rows):
{df.head(3).to_string()}

USER QUESTION: {message}

INSTRUCTIONS:
1. Answer the user's question DIRECTLY using the actual data shown above
2. Provide specific numbers, column names, and percentages from the real data
3. Call functions only if you need to create visualizations or perform operations
4. DO NOT give generic suggestions - use the ACTUAL data to answer
"""
        except:
            dataset_context = f"User message: {message}\n\nNote: No dataset loaded yet. If they're asking about data operations, suggest uploading a dataset first."
        
        try:
            # Generate response with function calling
            chat = self.model.start_chat()
            response = chat.send_message(dataset_context)
            
            function_calls_made = []
            results = []
            chart_data = None
            data_preview = None
            
            # Check if model wants to call functions
            if response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'function_call') and part.function_call:
                        fc = part.function_call
                        function_name = fc.name
                        function_args = dict(fc.args)
                        
                        function_calls_made.append(function_name)
                        
                        # Execute the function
                        try:
                            if function_name == "get_statistics":
                                result = self.data_processor.calculate_statistics(
                                    session_id,
                                    function_args.get('columns')
                                )
                                results.append(result)
                            
                            elif function_name == "detect_missing_values":
                                result = self.data_processor.detect_missing_values(session_id)
                                results.append(result)
                            
                            elif function_name == "get_correlation":
                                result = self.data_processor.calculate_correlation(
                                    session_id,
                                    function_args.get('columns')
                                )
                                results.append(result)
                                
                                # Also create a heatmap
                                chart_data = self.data_processor.create_visualization(
                                    session_id,
                                    chart_type="correlation",
                                    parameters={"title": "Correlation Matrix"}
                                )
                            
                            elif function_name == "create_visualization":
                                chart_data = self.data_processor.create_visualization(
                                    session_id,
                                    chart_type=function_args['chart_type'],
                                    x_column=function_args.get('x_column'),
                                    y_column=function_args.get('y_column'),
                                    parameters=function_args
                                )
                                results.append({"visualization": "created"})
                            
                            elif function_name == "clean_data":
                                result = self.data_processor.clean_data(
                                    session_id,
                                    parameters=function_args
                                )
                                results.append(result)
                                # Don't automatically show preview after cleaning
                                # Users can explicitly request to see the data if needed
                            
                            elif function_name == "show_data_preview":
                                # Get the current dataset and create a fresh preview
                                try:
                                    df = self.data_processor.get_dataframe(session_id)
                                    data_preview = self.data_processor._create_preview(df, max_rows=100)
                                    results.append({"message": "Showing data preview"})
                                except Exception as e:
                                    results.append({"error": "No dataset loaded"})
                            
                            elif function_name == "ml_analysis":
                                result = self.data_processor.ml_analysis(
                                    session_id,
                                    analysis_type=function_args['analysis_type'],
                                    parameters=function_args
                                )
                                results.append(result)
                                if result.get('visualization'):
                                    chart_data = result['visualization']
                            
                            elif function_name == "filter_data":
                                # Simple filtering
                                df = self.data_processor.get_dataframe(session_id)
                                col = function_args['column']
                                op = function_args['operator']
                                val = function_args['value']
                                
                                if op == '>':
                                    df_filtered = df[df[col] > val]
                                elif op == '<':
                                    df_filtered = df[df[col] < val]
                                elif op == '==':
                                    df_filtered = df[df[col] == val]
                                elif op == '!=':
                                    df_filtered = df[df[col] != val]
                                elif op == '>=':
                                    df_filtered = df[df[col] >= val]
                                elif op == '<=':
                                    df_filtered = df[df[col] <= val]
                                elif op == 'contains':
                                    df_filtered = df[df[col].astype(str).str.contains(str(val), case=False)]
                                else:
                                    df_filtered = df
                                
                                self.data_processor.update_dataframe(session_id, df_filtered)
                                results.append({
                                    "filtered_rows": len(df_filtered),
                                    "original_rows": len(df)
                                })
                        
                        except Exception as e:
                            results.append({"error": str(e)})
            
            # Get the text response
            if response.text:
                ai_message = response.text
            else:
                # Generate a follow-up response with the function results
                follow_up = chat.send_message(
                    f"I executed these functions: {', '.join(function_calls_made)}. "
                    f"Results: {json.dumps(results, default=str)}. "
                    "Please provide a natural language summary of the results for the user."
                )
                ai_message = follow_up.text
            
            # Generate suggested actions based on context
            suggested_actions = self._generate_suggestions(session_id, function_calls_made)
            
            return {
                "message": ai_message,
                "function_calls": function_calls_made if function_calls_made else None,
                "results": results if results else None,
                "data_preview": data_preview if data_preview else None,
                "chart_data": chart_data,
                "suggested_actions": suggested_actions
            }
        
        except Exception as e:
            return {
                "message": f"I encountered an error: {str(e)}. Could you please rephrase your request?",
                "function_calls": None,
                "results": None
            }
    
    async def _process_with_groq(
        self,
        session_id: str,
        message: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Process user message using Groq AI with tool calling"""
        
        if not groq_client:
            return {
                "message": "⚠️ Groq not configured.",
                "function_calls": None,
                "results": None
            }
        
        # Get dataset info for context
        try:
            df = self.data_processor.get_dataframe(session_id)
            
            # Get missing value info
            missing_info = []
            for col in df.columns:
                missing_count = df[col].isnull().sum()
                if missing_count > 0:
                    missing_pct = (missing_count / len(df)) * 100
                    missing_info.append(f"{col}: {missing_count} ({missing_pct:.1f}%)")
            
            # Get numeric column stats preview
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            stats_preview = []
            for col in numeric_cols[:5]:
                stats_preview.append(f"{col}: min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}")
            
            dataset_context = f"""
You are analyzing a dataset with the following ACTUAL data:

DATASET OVERVIEW:
- Total rows: {len(df)}
- Total columns: {len(df.columns)}

COLUMNS ({len(df.columns)} total):
{chr(10).join([f"- {col} ({df[col].dtype}): {df[col].nunique()} unique values" for col in df.columns])}

MISSING VALUES:
{chr(10).join([f"- {info}" for info in missing_info]) if missing_info else "- No missing values found"}

NUMERIC COLUMNS PREVIEW:
{chr(10).join([f"- {stat}" for stat in stats_preview]) if stats_preview else "- No numeric columns"}

DATA PREVIEW (first 3 rows):
{df.head(3).to_string()}

USER QUESTION: {message}

INSTRUCTIONS:
1. Answer the user's question DIRECTLY using the actual data shown above
2. Provide specific numbers, column names, and percentages from the real data
3. DO NOT give generic suggestions - use the ACTUAL data to answer
"""
        except:
            dataset_context = f"User message: {message}\n\nNote: No dataset loaded. Suggest uploading a dataset first."
        
        try:
            # Use Groq's chat completion (Groq uses OpenAI-compatible API but simpler function calling)
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful data analysis assistant. Analyze user requests and suggest appropriate data operations."},
                    {"role": "user", "content": dataset_context}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            
            ai_message = response.choices[0].message.content
            
            # Parse AI response for function calls (simple keyword matching for Groq)
            function_calls_made = []
            results = []
            chart_data = None
            data_preview = None
            
            # Detect if AI suggests statistics
            if any(keyword in ai_message.lower() for keyword in ['statistics', 'summary', 'mean', 'median', 'std']):
                try:
                    result = self.data_processor.calculate_statistics(session_id)
                    results.append(result)
                    function_calls_made.append('get_statistics')
                except Exception as e:
                    results.append({"error": str(e)})
            
            # Detect if AI suggests visualization
            chart_keywords = {
                'histogram': 'histogram',
                'scatter plot': 'scatter',
                'bar chart': 'bar',
                'line chart': 'line',
                'correlation': 'correlation',
                'heatmap': 'heatmap'
            }
            
            for keyword, chart_type in chart_keywords.items():
                if keyword in ai_message.lower():
                    try:
                        df = self.data_processor.get_dataframe(session_id)
                        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                        
                        if chart_type == 'histogram' and len(numeric_cols) >= 1:
                            chart_data = self.data_processor.create_visualization(
                                session_id,
                                chart_type='histogram',
                                x_column=numeric_cols[0],
                                parameters={"title": f"Distribution of {numeric_cols[0]}"}
                            )
                        elif chart_type in ['scatter', 'line', 'bar'] and len(numeric_cols) >= 2:
                            chart_data = self.data_processor.create_visualization(
                                session_id,
                                chart_type=chart_type,
                                x_column=numeric_cols[0],
                                y_column=numeric_cols[1],
                                parameters={"title": f"{chart_type.title()} Chart"}
                            )
                        elif chart_type == 'correlation':
                            chart_data = self.data_processor.create_visualization(
                                session_id,
                                chart_type='correlation',
                                parameters={"title": "Correlation Matrix"}
                            )
                        
                        function_calls_made.append('create_visualization')
                        results.append({"visualization": "created"})
                        break
                    except Exception as e:
                        results.append({"error": str(e)})
            
            # Detect cleaning operations
            if any(keyword in ai_message.lower() for keyword in ['missing', 'impute', 'fill']):
                try:
                    result = self.data_processor.clean_data(
                        session_id,
                        parameters={
                            "handleMissing": True,
                            "missingMethod": "mean"
                        }
                    )
                    results.append(result)
                    # Don't automatically show preview after cleaning
                    # Users can explicitly request to see the data if needed
                    function_calls_made.append('clean_data')
                except Exception as e:
                    results.append({"error": str(e)})
            
            # Detect data preview requests
            show_keywords = ['show data', 'display data', 'view data', 'show table', 'display table', 
                           'view table', 'see data', 'see table', 'preview data', 'show me the data']
            if any(keyword in ai_message.lower() for keyword in show_keywords):
                try:
                    df = self.data_processor.get_dataframe(session_id)
                    data_preview = self.data_processor._create_preview(df, max_rows=100)
                    results.append({"message": "Showing data preview"})
                    function_calls_made.append('show_data_preview')
                except Exception as e:
                    results.append({"error": "No dataset loaded"})
            
            # Generate suggested actions
            suggested_actions = self._generate_suggestions(session_id, function_calls_made)
            
            return {
                "message": ai_message,
                "function_calls": function_calls_made if function_calls_made else None,
                "results": results if results else None,
                "data_preview": data_preview if data_preview else None,
                "chart_data": chart_data,
                "suggested_actions": suggested_actions,
                "provider": "groq"
            }
        
        except Exception as e:
            return {
                "message": f"I encountered an error: {str(e)}. Could you please rephrase your request?",
                "function_calls": None,
                "results": None,
                "error": str(e)
            }
    
    def _generate_suggestions(self, session_id: str, recent_actions: List[str]) -> List[Dict[str, str]]:
        """Generate context-aware suggestions"""
        
        suggestions = []
        
        try:
            df = self.data_processor.get_dataframe(session_id)
            quality = self.data_processor.sessions[session_id].get('quality', {})
            
            # Suggest based on data quality
            if quality.get('issues'):
                for issue in quality['issues'][:2]:
                    if issue['type'] == 'missing_values':
                        suggestions.append({
                            "label": "Handle Missing Values",
                            "prompt": "Handle missing values using mean imputation"
                        })
                    elif issue['type'] == 'duplicates':
                        suggestions.append({
                            "label": "Remove Duplicates",
                            "prompt": "Remove duplicate rows"
                        })
                    elif issue['type'] == 'outliers':
                        suggestions.append({
                            "label": "Detect Outliers",
                            "prompt": f"Detect outliers in {issue.get('column', 'numeric columns')}"
                        })
            
            # General suggestions
            if 'get_statistics' not in recent_actions:
                suggestions.append({
                    "label": "Show Statistics",
                    "prompt": "Show statistical summary of all columns"
                })
            
            if 'get_correlation' not in recent_actions:
                suggestions.append({
                    "label": "Correlation Analysis",
                    "prompt": "Show correlation matrix"
                })
            
            if 'create_visualization' not in recent_actions:
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                if len(numeric_cols) >= 2:
                    suggestions.append({
                        "label": "Create Scatter Plot",
                        "prompt": f"Create scatter plot of {numeric_cols[0]} vs {numeric_cols[1]}"
                    })
            
            if 'ml_analysis' not in recent_actions:
                suggestions.append({
                    "label": "Cluster Analysis",
                    "prompt": "Perform K-means clustering with 3 clusters"
                })
        
        except:
            # Default suggestions if no dataset
            suggestions = [
                {"label": "Upload Data", "prompt": "How do I upload a dataset?"},
                {"label": "Get Started", "prompt": "What can you help me with?"}
            ]
        
        return suggestions[:5]  # Return top 5
