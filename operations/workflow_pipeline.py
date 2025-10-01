"""
Data Transformation Pipelines
Saved workflows and scheduling capabilities
"""

import pandas as pd
import json
from typing import List, Dict, Optional, Callable, Tuple
from datetime import datetime
import uuid


class PipelineStep:
    """Represents a single step in a data transformation pipeline"""
    
    def __init__(self, step_id: str, name: str, operation: str, parameters: Dict):
        self.step_id = step_id
        self.name = name
        self.operation = operation
        self.parameters = parameters
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict:
        """Convert step to dictionary"""
        return {
            'step_id': self.step_id,
            'name': self.name,
            'operation': self.operation,
            'parameters': self.parameters,
            'timestamp': self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PipelineStep':
        """Create step from dictionary"""
        step = cls(
            data['step_id'],
            data['name'],
            data['operation'],
            data['parameters']
        )
        step.timestamp = data.get('timestamp', datetime.now().isoformat())
        return step


class Pipeline:
    """Represents a data transformation pipeline"""
    
    def __init__(self, pipeline_id: str, name: str, description: str = ""):
        self.pipeline_id = pipeline_id
        self.name = name
        self.description = description
        self.steps: List[PipelineStep] = []
        self.created = datetime.now().isoformat()
        self.last_modified = datetime.now().isoformat()
        self.execution_history: List[Dict] = []
    
    def add_step(self, name: str, operation: str, parameters: Dict) -> PipelineStep:
        """Add a step to the pipeline"""
        step_id = str(uuid.uuid4())
        step = PipelineStep(step_id, name, operation, parameters)
        self.steps.append(step)
        self.last_modified = datetime.now().isoformat()
        return step
    
    def remove_step(self, step_id: str) -> bool:
        """Remove a step from the pipeline"""
        for i, step in enumerate(self.steps):
            if step.step_id == step_id:
                self.steps.pop(i)
                self.last_modified = datetime.now().isoformat()
                return True
        return False
    
    def reorder_steps(self, step_ids: List[str]):
        """Reorder steps based on provided order"""
        step_dict = {step.step_id: step for step in self.steps}
        self.steps = [step_dict[sid] for sid in step_ids if sid in step_dict]
        self.last_modified = datetime.now().isoformat()
    
    def execute(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        Execute the pipeline on a DataFrame
        
        Args:
            df: Input DataFrame
        
        Returns:
            Tuple[pd.DataFrame, Dict]: Transformed DataFrame and execution report
        """
        from operations.cleaning import DataCleaner
        from operations.imputation import MissingValueImputer
        from operations.encoding import CategoricalEncoder
        from operations.ml_cleaning import MLDataCleaner
        
        result_df = df.copy()
        execution_log = []
        errors = []
        
        cleaner = DataCleaner()
        imputer = MissingValueImputer()
        encoder = CategoricalEncoder()
        ml_cleaner = MLDataCleaner()
        
        start_time = datetime.now()
        
        for step in self.steps:
            step_start = datetime.now()
            
            try:
                operation = step.operation
                params = step.parameters
                
                if operation == 'remove_duplicates':
                    before = len(result_df)
                    result_df = result_df.drop_duplicates()
                    removed = before - len(result_df)
                    execution_log.append({
                        'step': step.name,
                        'operation': operation,
                        'result': f'Removed {removed} duplicates',
                        'status': 'success'
                    })
                
                elif operation == 'drop_columns':
                    columns = params.get('columns', [])
                    result_df = result_df.drop(columns=columns, errors='ignore')
                    execution_log.append({
                        'step': step.name,
                        'operation': operation,
                        'result': f'Dropped {len(columns)} columns',
                        'status': 'success'
                    })
                
                elif operation == 'impute':
                    column = params.get('column')
                    method = params.get('method', 'Mean')
                    if column and column in result_df.columns:
                        result_df = imputer.impute_column(result_df, column, method, **params)
                        execution_log.append({
                            'step': step.name,
                            'operation': operation,
                            'result': f'Imputed {column} using {method}',
                            'status': 'success'
                        })
                
                elif operation == 'encode':
                    column = params.get('column')
                    encoding_type = params.get('type', 'label')
                    if column and column in result_df.columns:
                        if encoding_type == 'label':
                            result_df = encoder.label_encode(result_df, column)
                        elif encoding_type == 'onehot':
                            result_df = encoder.onehot_encode(result_df, [column], params.get('drop_first', True))
                        execution_log.append({
                            'step': step.name,
                            'operation': operation,
                            'result': f'Encoded {column} using {encoding_type}',
                            'status': 'success'
                        })
                
                elif operation == 'detect_outliers':
                    column = params.get('column')
                    method = params.get('method', 'iqr')
                    if column and column in result_df.columns:
                        outliers = cleaner.detect_outliers(result_df, column, method=method, **params)
                        outlier_count = int(outliers.sum())
                        execution_log.append({
                            'step': step.name,
                            'operation': operation,
                            'result': f'Detected {outlier_count} outliers in {column}',
                            'status': 'success'
                        })
                
                elif operation == 'remove_outliers':
                    column = params.get('column')
                    method = params.get('method', 'iqr')
                    if column and column in result_df.columns:
                        outliers = cleaner.detect_outliers(result_df, column, method=method, **params)
                        outlier_count = int(outliers.sum())
                        filtered_df = result_df[~outliers]
                        assert isinstance(filtered_df, pd.DataFrame)
                        result_df = filtered_df
                        execution_log.append({
                            'step': step.name,
                            'operation': operation,
                            'result': f'Removed {outlier_count} outliers from {column}',
                            'status': 'success'
                        })
                
                elif operation == 'ml_anomaly_detection':
                    contamination = params.get('contamination', 0.1)
                    selected_cols = params.get('columns', None)
                    result_df, anomaly_info = ml_cleaner.detect_anomalies_multivariate(
                        result_df, contamination, selected_cols
                    )
                    execution_log.append({
                        'step': step.name,
                        'operation': operation,
                        'result': f"Detected {anomaly_info.get('total_anomalies', 0)} anomalies",
                        'status': 'success'
                    })
                
                elif operation == 'auto_clean':
                    cleaned_df, ops = cleaner.auto_clean(result_df)
                    result_df = cleaned_df
                    execution_log.append({
                        'step': step.name,
                        'operation': operation,
                        'result': f'Applied {len(ops)} auto-clean operations',
                        'status': 'success'
                    })
                
                elif operation == 'filter_rows':
                    condition = params.get('condition')
                    if condition:
                        before = len(result_df)
                        result_df = result_df.query(condition)
                        removed = before - len(result_df)
                        execution_log.append({
                            'step': step.name,
                            'operation': operation,
                            'result': f'Filtered {removed} rows',
                            'status': 'success'
                        })
                
                elif operation == 'transform_column':
                    column = params.get('column')
                    transformation = params.get('transformation', 'log')
                    if column and column in result_df.columns:
                        import numpy as np
                        if transformation == 'log':
                            result_df[column] = np.log1p(result_df[column])
                        elif transformation == 'sqrt':
                            result_df[column] = np.sqrt(result_df[column])
                        elif transformation == 'square':
                            result_df[column] = result_df[column] ** 2
                        execution_log.append({
                            'step': step.name,
                            'operation': operation,
                            'result': f'Applied {transformation} to {column}',
                            'status': 'success'
                        })
                
            except Exception as e:
                errors.append({
                    'step': step.name,
                    'operation': step.operation,
                    'error': str(e)
                })
                execution_log.append({
                    'step': step.name,
                    'operation': step.operation,
                    'result': f'Error: {str(e)}',
                    'status': 'error'
                })
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        execution_report = {
            'pipeline_id': self.pipeline_id,
            'pipeline_name': self.name,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration_seconds': duration,
            'total_steps': len(self.steps),
            'successful_steps': len([log for log in execution_log if log['status'] == 'success']),
            'failed_steps': len(errors),
            'execution_log': execution_log,
            'errors': errors,
            'input_shape': df.shape,
            'output_shape': result_df.shape
        }
        
        # Add to execution history
        self.execution_history.append(execution_report)
        
        return result_df, execution_report
    
    def to_dict(self) -> Dict:
        """Convert pipeline to dictionary"""
        return {
            'pipeline_id': self.pipeline_id,
            'name': self.name,
            'description': self.description,
            'steps': [step.to_dict() for step in self.steps],
            'created': self.created,
            'last_modified': self.last_modified,
            'execution_history': self.execution_history[-10:]  # Keep last 10 executions
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Pipeline':
        """Create pipeline from dictionary"""
        pipeline = cls(
            data['pipeline_id'],
            data['name'],
            data.get('description', '')
        )
        pipeline.created = data.get('created', datetime.now().isoformat())
        pipeline.last_modified = data.get('last_modified', datetime.now().isoformat())
        pipeline.steps = [PipelineStep.from_dict(step_data) for step_data in data.get('steps', [])]
        pipeline.execution_history = data.get('execution_history', [])
        return pipeline


class WorkflowManager:
    """Manage data transformation workflows and pipelines"""
    
    def __init__(self):
        self.pipelines: Dict[str, Pipeline] = {}
    
    def create_pipeline(self, name: str, description: str = "") -> Pipeline:
        """Create a new pipeline"""
        pipeline_id = str(uuid.uuid4())
        pipeline = Pipeline(pipeline_id, name, description)
        self.pipelines[pipeline_id] = pipeline
        return pipeline
    
    def delete_pipeline(self, pipeline_id: str) -> bool:
        """Delete a pipeline"""
        if pipeline_id in self.pipelines:
            del self.pipelines[pipeline_id]
            return True
        return False
    
    def get_pipeline(self, pipeline_id: str) -> Optional[Pipeline]:
        """Get a pipeline by ID"""
        return self.pipelines.get(pipeline_id)
    
    def list_pipelines(self) -> List[Dict]:
        """List all pipelines"""
        return [
            {
                'pipeline_id': p.pipeline_id,
                'name': p.name,
                'description': p.description,
                'steps_count': len(p.steps),
                'created': p.created,
                'last_modified': p.last_modified
            }
            for p in self.pipelines.values()
        ]
    
    def save_pipeline(self, pipeline: Pipeline, filepath: str) -> Tuple[bool, str]:
        """Save pipeline to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(pipeline.to_dict(), f, indent=2)
            return True, "Pipeline saved successfully"
        except Exception as e:
            return False, f"Error saving pipeline: {str(e)}"
    
    def load_pipeline(self, filepath: str) -> Optional[Pipeline]:
        """Load pipeline from file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            pipeline = Pipeline.from_dict(data)
            self.pipelines[pipeline.pipeline_id] = pipeline
            return pipeline
        except Exception as e:
            print(f"Error loading pipeline: {str(e)}")
            return None
    
    def duplicate_pipeline(self, pipeline_id: str, new_name: str) -> Optional[Pipeline]:
        """Duplicate an existing pipeline"""
        original = self.get_pipeline(pipeline_id)
        if not original:
            return None
        
        new_pipeline = self.create_pipeline(new_name, original.description)
        for step in original.steps:
            new_pipeline.add_step(step.name, step.operation, step.parameters.copy())
        
        return new_pipeline
    
    def get_predefined_pipelines(self) -> Dict[str, Pipeline]:
        """Get predefined pipelines for common tasks"""
        pipelines = {}
        
        # Basic Data Cleaning Pipeline
        basic = self.create_pipeline(
            "Basic Data Cleaning",
            "Standard cleaning workflow for most datasets"
        )
        basic.add_step("Remove Duplicates", "remove_duplicates", {})
        basic.add_step("Auto Clean", "auto_clean", {})
        pipelines['basic'] = basic
        
        # ML Preparation Pipeline
        ml_prep = self.create_pipeline(
            "ML Preparation",
            "Prepare data for machine learning"
        )
        ml_prep.add_step("Remove Duplicates", "remove_duplicates", {})
        ml_prep.add_step("Detect Anomalies", "ml_anomaly_detection", {'contamination': 0.1})
        pipelines['ml_prep'] = ml_prep
        
        # Advanced Cleaning Pipeline
        advanced = self.create_pipeline(
            "Advanced Cleaning",
            "Comprehensive cleaning with outlier detection"
        )
        advanced.add_step("Remove Duplicates", "remove_duplicates", {})
        advanced.add_step("Auto Clean", "auto_clean", {})
        advanced.add_step("Detect Anomalies", "ml_anomaly_detection", {'contamination': 0.1})
        pipelines['advanced'] = advanced
        
        return pipelines
