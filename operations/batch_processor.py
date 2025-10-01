"""
Batch Processing Module
Process multiple files with automated cleaning templates
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Callable
import json
from datetime import datetime
import io


class CleaningTemplate:
    """Represents a reusable cleaning template"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.steps = []
    
    def add_step(self, operation: str, parameters: Dict):
        """Add a cleaning step to the template"""
        self.steps.append({
            'operation': operation,
            'parameters': parameters,
            'timestamp': datetime.now().isoformat()
        })
    
    def to_dict(self) -> Dict:
        """Convert template to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'steps': self.steps,
            'created': datetime.now().isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CleaningTemplate':
        """Create template from dictionary"""
        template = cls(data['name'], data.get('description', ''))
        template.steps = data.get('steps', [])
        return template


class BatchProcessor:
    """Process multiple files with automated cleaning templates"""
    
    def __init__(self):
        self.templates = {}
        self.batch_results = []
    
    def create_template(self, name: str, description: str = "") -> CleaningTemplate:
        """Create a new cleaning template"""
        template = CleaningTemplate(name, description)
        self.templates[name] = template
        return template
    
    def save_template(self, template: CleaningTemplate, filepath: str):
        """Save template to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(template.to_dict(), f, indent=2)
            return True, "Template saved successfully"
        except Exception as e:
            return False, f"Error saving template: {str(e)}"
    
    def load_template(self, filepath: str) -> Optional[CleaningTemplate]:
        """Load template from file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            template = CleaningTemplate.from_dict(data)
            self.templates[template.name] = template
            return template
        except Exception as e:
            print(f"Error loading template: {str(e)}")
            return None
    
    def apply_template(self, df: pd.DataFrame, template: CleaningTemplate) -> Tuple[pd.DataFrame, List[str]]:
        """
        Apply a cleaning template to a DataFrame
        
        Args:
            df: DataFrame to clean
            template: Cleaning template to apply
        
        Returns:
            Tuple[pd.DataFrame, List[str]]: Cleaned DataFrame and operations log
        """
        from operations.cleaning import DataCleaner
        from operations.imputation import MissingValueImputer
        from operations.encoding import CategoricalEncoder
        
        cleaned_df = df.copy()
        operations_log = []
        
        cleaner = DataCleaner()
        imputer = MissingValueImputer()
        encoder = CategoricalEncoder()
        
        for step in template.steps:
            operation = step['operation']
            params = step['parameters']
            
            try:
                if operation == 'remove_duplicates':
                    before_count = len(cleaned_df)
                    cleaned_df = cleaned_df.drop_duplicates()
                    removed = before_count - len(cleaned_df)
                    operations_log.append(f"Removed {removed} duplicate rows")
                
                elif operation == 'drop_columns':
                    columns = params.get('columns', [])
                    cleaned_df = cleaned_df.drop(columns=columns, errors='ignore')
                    operations_log.append(f"Dropped columns: {', '.join(columns)}")
                
                elif operation == 'drop_high_missing':
                    threshold = params.get('threshold', 0.5)
                    cols_to_drop = []
                    for col in cleaned_df.columns:
                        missing_pct = cleaned_df[col].isnull().sum() / len(cleaned_df)
                        if missing_pct > threshold:
                            cols_to_drop.append(col)
                    if cols_to_drop:
                        cleaned_df = cleaned_df.drop(columns=cols_to_drop)
                        operations_log.append(f"Dropped {len(cols_to_drop)} columns with >{threshold*100}% missing values")
                
                elif operation == 'impute':
                    column = params.get('column')
                    method = params.get('method', 'Mean')
                    if column and column in cleaned_df.columns:
                        cleaned_df = imputer.impute_column(cleaned_df, column, method)
                        operations_log.append(f"Imputed {column} using {method}")
                
                elif operation == 'fill_na':
                    value = params.get('value', 0)
                    cleaned_df = cleaned_df.fillna(value)
                    operations_log.append(f"Filled missing values with {value}")
                
                elif operation == 'strip_whitespace':
                    text_cols = cleaned_df.select_dtypes(include=['object']).columns
                    for col in text_cols:
                        cleaned_df[col] = cleaned_df[col].str.strip() if cleaned_df[col].dtype == 'object' else cleaned_df[col]
                    operations_log.append(f"Stripped whitespace from {len(text_cols)} text columns")
                
                elif operation == 'lowercase':
                    columns = params.get('columns', [])
                    for col in columns:
                        if col in cleaned_df.columns and cleaned_df[col].dtype == 'object':
                            cleaned_df[col] = cleaned_df[col].str.lower()
                    operations_log.append(f"Converted to lowercase: {', '.join(columns)}")
                
                elif operation == 'uppercase':
                    columns = params.get('columns', [])
                    for col in columns:
                        if col in cleaned_df.columns and cleaned_df[col].dtype == 'object':
                            cleaned_df[col] = cleaned_df[col].str.upper()
                    operations_log.append(f"Converted to uppercase: {', '.join(columns)}")
                
                elif operation == 'label_encode':
                    column = params.get('column')
                    if column and column in cleaned_df.columns:
                        cleaned_df = encoder.label_encode(cleaned_df, column)
                        operations_log.append(f"Label encoded {column}")
                
                elif operation == 'onehot_encode':
                    columns = params.get('columns', [])
                    columns = [col for col in columns if col in cleaned_df.columns]
                    if columns:
                        cleaned_df = encoder.onehot_encode(cleaned_df, columns, params.get('drop_first', True))
                        operations_log.append(f"One-hot encoded {', '.join(columns)}")
                
                elif operation == 'remove_outliers':
                    column = params.get('column')
                    method = params.get('method', 'iqr')
                    if column and column in cleaned_df.columns:
                        outliers = cleaner.detect_outliers(cleaned_df, column, method=method, **params)
                        cleaned_df = cleaned_df[~outliers]
                        operations_log.append(f"Removed {outliers.sum()} outliers from {column}")
                
                elif operation == 'convert_dtype':
                    column = params.get('column')
                    dtype = params.get('dtype')
                    if column and column in cleaned_df.columns and dtype:
                        cleaned_df[column] = cleaned_df[column].astype(dtype)
                        operations_log.append(f"Converted {column} to {dtype}")
                
                elif operation == 'rename_columns':
                    mapping = params.get('mapping', {})
                    cleaned_df = cleaned_df.rename(columns=mapping)
                    operations_log.append(f"Renamed columns: {mapping}")
                
                elif operation == 'auto_clean':
                    auto_df, auto_ops = cleaner.auto_clean(cleaned_df)
                    cleaned_df = auto_df
                    operations_log.extend(auto_ops)
                
            except Exception as e:
                operations_log.append(f"Error in {operation}: {str(e)}")
        
        return cleaned_df, operations_log
    
    def process_files(self, files: List, template: Optional[CleaningTemplate] = None,
                     output_format: str = 'csv') -> List[Dict]:
        """
        Process multiple files with optional template
        
        Args:
            files: List of file objects or paths
            template: Optional cleaning template
            output_format: Output file format
        
        Returns:
            List[Dict]: Processing results for each file
        """
        results = []
        
        for file_obj in files:
            result = {
                'filename': file_obj.name if hasattr(file_obj, 'name') else str(file_obj),
                'status': 'pending',
                'operations': [],
                'errors': []
            }
            
            try:
                # Load file
                if hasattr(file_obj, 'name'):
                    filename = file_obj.name
                    if filename.endswith('.csv'):
                        df = pd.read_csv(file_obj)
                    elif filename.endswith(('.xlsx', '.xls')):
                        df = pd.read_excel(file_obj)
                    elif filename.endswith('.json'):
                        df = pd.read_json(file_obj)
                    elif filename.endswith('.parquet'):
                        df = pd.read_parquet(file_obj)
                    else:
                        result['status'] = 'error'
                        result['errors'].append('Unsupported file format')
                        results.append(result)
                        continue
                else:
                    result['status'] = 'error'
                    result['errors'].append('Invalid file object')
                    results.append(result)
                    continue
                
                result['rows_before'] = len(df)
                result['columns_before'] = len(df.columns)
                
                # Apply template if provided
                if template:
                    df, operations = self.apply_template(df, template)
                    result['operations'] = operations
                
                result['rows_after'] = len(df)
                result['columns_after'] = len(df.columns)
                result['processed_data'] = df
                result['status'] = 'success'
                
            except Exception as e:
                result['status'] = 'error'
                result['errors'].append(str(e))
            
            results.append(result)
        
        self.batch_results = results
        return results
    
    def get_predefined_templates(self) -> Dict[str, CleaningTemplate]:
        """Get predefined cleaning templates"""
        templates = {}
        
        # Basic cleaning template
        basic = CleaningTemplate(
            "Basic Cleaning",
            "Remove duplicates, drop high missing columns, strip whitespace"
        )
        basic.add_step('remove_duplicates', {})
        basic.add_step('drop_high_missing', {'threshold': 0.8})
        basic.add_step('strip_whitespace', {})
        templates['basic'] = basic
        
        # Standard cleaning template
        standard = CleaningTemplate(
            "Standard Cleaning",
            "Comprehensive cleaning with imputation"
        )
        standard.add_step('remove_duplicates', {})
        standard.add_step('drop_high_missing', {'threshold': 0.95})
        standard.add_step('strip_whitespace', {})
        standard.add_step('auto_clean', {})
        templates['standard'] = standard
        
        # Text cleaning template
        text = CleaningTemplate(
            "Text Cleaning",
            "Clean and standardize text columns"
        )
        text.add_step('strip_whitespace', {})
        text.add_step('lowercase', {'columns': []})
        text.add_step('remove_duplicates', {})
        templates['text'] = text
        
        # Numeric cleaning template
        numeric = CleaningTemplate(
            "Numeric Cleaning",
            "Handle missing values and outliers in numeric data"
        )
        numeric.add_step('drop_high_missing', {'threshold': 0.5})
        numeric.add_step('fill_na', {'value': 0})
        templates['numeric'] = numeric
        
        self.templates.update(templates)
        return templates
    
    def export_results(self, results: List[Dict], output_format: str = 'csv') -> List[bytes]:
        """
        Export processed results
        
        Args:
            results: Processing results
            output_format: Output format
        
        Returns:
            List[bytes]: List of file contents
        """
        exports = []
        
        for result in results:
            if result['status'] == 'success' and 'processed_data' in result:
                df = result['processed_data']
                buffer = io.BytesIO()
                
                if output_format == 'csv':
                    df.to_csv(buffer, index=False)
                elif output_format == 'excel':
                    df.to_excel(buffer, index=False)
                elif output_format == 'json':
                    df.to_json(buffer, orient='records')
                elif output_format == 'parquet':
                    df.to_parquet(buffer, index=False)
                
                exports.append(buffer.getvalue())
        
        return exports
