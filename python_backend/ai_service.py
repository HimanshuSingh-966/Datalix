import os
import json
from typing import Dict, Any, List, Optional
import google.generativeai as genai
import google.ai.generativelanguage as glm
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
    print("⚠️  Warning: GEMINI_API_KEY not set. AI features will not work.")

class AIService:
    def __init__(self, data_processor: DataProcessor):
        """Initialize AI service with shared data processor instance."""
        self.data_processor = data_processor
        
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
        user_id: str
    ) -> Dict[str, Any]:
        """Process user message using Gemini AI with function calling"""
        
        if not self.model:
            return {
                "message": "⚠️ AI service not configured. Please set GEMINI_API_KEY environment variable.",
                "function_calls": None,
                "results": None
            }
        
        # Get dataset info for context
        try:
            df = self.data_processor.get_dataframe(session_id)
            dataset_context = f"""
You are analyzing a dataset with:
- {len(df)} rows
- {len(df.columns)} columns
- Column names: {', '.join(df.columns.tolist())}
- Column types: {', '.join([f"{col} ({df[col].dtype})" for col in df.columns[:10]])}

The user wants: {message}

Analyze what they need and call the appropriate function(s) to help them.
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
                                data_preview = result.get('preview')
                            
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
                "data_preview": data_preview,
                "chart_data": chart_data,
                "suggested_actions": suggested_actions
            }
        
        except Exception as e:
            return {
                "message": f"I encountered an error: {str(e)}. Could you please rephrase your request?",
                "function_calls": None,
                "results": None
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
