import os
import json
from typing import Dict, Any, List, Optional
import google.generativeai as genai
from data_processor import DataProcessor
from statistics_module import calculate_statistics, calculate_correlation
from visualizations import create_visualization
from data_cleaning import clean_dataset, handle_missing_values
from ml_analysis import perform_ml_analysis

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️  Warning: GEMINI_API_KEY not set. AI features will not work.")

class AIService:
    def __init__(self, data_processor: DataProcessor):
        """Initialize AI service with shared data processor instance."""
        self.data_processor = data_processor
        
        # Define function declarations for Gemini
        self.functions = [
            {
                "name": "get_statistics",
                "description": "Calculate statistical summary (mean, median, std, min, max, quartiles) for numeric columns in the dataset",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "columns": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific columns to analyze. If not provided, analyzes all numeric columns"
                        }
                    }
                }
            },
            {
                "name": "get_correlation",
                "description": "Calculate correlation matrix showing relationships between numeric variables",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "columns": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Specific columns to include in correlation. If not provided, uses all numeric columns"
                        }
                    }
                }
            },
            {
                "name": "create_visualization",
                "description": "Create various types of charts and plots (histogram, scatter, line, bar, box, violin, heatmap, correlation, pie, etc.)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "chart_type": {
                            "type": "string",
                            "enum": ["histogram", "scatter", "line", "bar", "box", "violin", "heatmap", "correlation", "pie", "donut", "treemap", "sunburst", "3d_scatter"],
                            "description": "Type of chart to create"
                        },
                        "x_column": {
                            "type": "string",
                            "description": "Column for X-axis"
                        },
                        "y_column": {
                            "type": "string",
                            "description": "Column for Y-axis"
                        },
                        "title": {
                            "type": "string",
                            "description": "Chart title"
                        },
                        "colorBy": {
                            "type": "string",
                            "description": "Column to use for color coding"
                        }
                    },
                    "required": ["chart_type"]
                }
            },
            {
                "name": "clean_data",
                "description": "Clean the dataset by handling missing values, removing outliers, removing duplicates, or normalizing data",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "handleMissing": {
                            "type": "boolean",
                            "description": "Whether to handle missing values"
                        },
                        "missingMethod": {
                            "type": "string",
                            "enum": ["drop", "mean", "median", "mode", "forward_fill", "backward_fill", "knn", "interpolation"],
                            "description": "Method to handle missing values"
                        },
                        "removeDuplicates": {
                            "type": "boolean",
                            "description": "Whether to remove duplicate rows"
                        },
                        "handleOutliers": {
                            "type": "boolean",
                            "description": "Whether to handle outliers"
                        },
                        "outlierMethod": {
                            "type": "string",
                            "enum": ["iqr", "zscore"],
                            "description": "Method to detect outliers"
                        },
                        "outlierAction": {
                            "type": "string",
                            "enum": ["remove", "cap", "flag"],
                            "description": "What to do with detected outliers"
                        }
                    }
                }
            },
            {
                "name": "ml_analysis",
                "description": "Perform machine learning analysis: anomaly detection, clustering, dimensionality reduction (PCA/t-SNE), or feature importance",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "analysis_type": {
                            "type": "string",
                            "enum": ["anomaly_detection", "clustering", "dimensionality_reduction", "feature_importance"],
                            "description": "Type of ML analysis to perform"
                        },
                        "algorithm": {
                            "type": "string",
                            "description": "Specific algorithm (e.g., 'kmeans', 'dbscan' for clustering, 'pca', 'tsne' for dimensionality reduction)"
                        },
                        "n_clusters": {
                            "type": "integer",
                            "description": "Number of clusters for clustering algorithms"
                        },
                        "contamination": {
                            "type": "number",
                            "description": "Expected proportion of anomalies (for anomaly detection)"
                        }
                    },
                    "required": ["analysis_type"]
                }
            },
            {
                "name": "filter_data",
                "description": "Filter dataset based on conditions (greater than, less than, equals, contains, etc.)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "column": {
                            "type": "string",
                            "description": "Column to filter on"
                        },
                        "operator": {
                            "type": "string",
                            "enum": [">", "<", "==", "!=", ">=", "<=", "contains"],
                            "description": "Comparison operator"
                        },
                        "value": {
                            "description": "Value to compare against"
                        }
                    },
                    "required": ["column", "operator", "value"]
                }
            }
        ]
        
        # Initialize Gemini model with function calling
        if GEMINI_API_KEY:
            self.model = genai.GenerativeModel(
                'gemini-1.5-flash',
                tools=self.functions
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
