"""
Advanced ML-based Data Cleaning
Includes anomaly detection, pattern recognition, and smart suggestions
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from typing import List, Dict, Tuple, Optional
import re


class MLDataCleaner:
    """Advanced ML-based data cleaning with intelligent suggestions"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.suggestions = []
    
    def detect_anomalies_multivariate(self, df: pd.DataFrame, 
                                     contamination: float = 0.1,
                                     selected_columns: Optional[List[str]] = None) -> Tuple[pd.DataFrame, Dict]:
        """
        Detect anomalies across multiple variables using Isolation Forest
        
        Args:
            df: DataFrame
            contamination: Expected proportion of outliers
            selected_columns: Specific columns to analyze
        
        Returns:
            Tuple[pd.DataFrame, Dict]: DataFrame with anomaly scores and detection results
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if selected_columns:
            numeric_cols = [col for col in selected_columns if col in numeric_cols]
        
        if not numeric_cols:
            return df, {'message': 'No numeric columns found for analysis'}
        
        # Prepare data
        X = df[numeric_cols].copy()
        X = X.fillna(X.mean())
        
        # Fit Isolation Forest
        iso_forest = IsolationForest(contamination=contamination, random_state=42)  # type: ignore
        anomaly_labels = iso_forest.fit_predict(X)
        anomaly_scores = iso_forest.score_samples(X)
        
        # Create result DataFrame
        result_df = df.copy()
        result_df['anomaly_label'] = anomaly_labels
        result_df['anomaly_score'] = anomaly_scores
        
        anomaly_count = (anomaly_labels == -1).sum()
        
        return result_df, {
            'total_anomalies': int(anomaly_count),
            'anomaly_percentage': float(anomaly_count / len(df) * 100),
            'analyzed_columns': numeric_cols,
            'contamination': contamination
        }
    
    def detect_pattern_anomalies(self, df: pd.DataFrame, column: str) -> Dict:
        """
        Detect pattern-based anomalies in text columns
        
        Args:
            df: DataFrame
            column: Column name to analyze
        
        Returns:
            Dict: Pattern analysis results
        """
        if column not in df.columns:
            return {'error': f'Column {column} not found'}
        
        if df[column].dtype != 'object':
            return {'error': f'Column {column} is not text type'}
        
        # Analyze patterns
        col_data = df[column].dropna().astype(str)
        
        # Common patterns
        patterns = {
            'email': r'^[\w\.-]+@[\w\.-]+\.\w+$',
            'phone': r'^[\+\d]?[\d\s\-\(\)]{7,}$',
            'url': r'^https?://[\w\.-]+\.\w+',
            'date': r'^\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}$',
            'numeric': r'^\d+\.?\d*$',
            'alphanumeric': r'^[a-zA-Z0-9]+$'
        }
        
        pattern_matches = {}
        for pattern_name, pattern_regex in patterns.items():
            matches = col_data.str.match(pattern_regex, na=False)
            match_count = matches.sum()
            if match_count > 0:
                pattern_matches[pattern_name] = {
                    'count': int(match_count),
                    'percentage': float(match_count / len(col_data) * 100)
                }
        
        # Detect inconsistent patterns
        unique_patterns = col_data.apply(lambda x: len(str(x))).value_counts()
        pattern_consistency = len(unique_patterns) / len(col_data) * 100
        
        # Detect common issues
        issues = []
        if col_data.str.contains(r'^\s|\s$', na=False).any():
            issues.append('Leading/trailing whitespace detected')
        if col_data.str.contains(r'\s{2,}', na=False).any():
            issues.append('Multiple consecutive spaces detected')
        if col_data.str.contains(r'[^\x00-\x7F]', na=False).any():
            issues.append('Non-ASCII characters detected')
        
        return {
            'pattern_matches': pattern_matches,
            'pattern_consistency_score': float(100 - pattern_consistency),
            'total_values': len(col_data),
            'unique_values': int(col_data.nunique()),
            'issues': issues
        }
    
    def cluster_based_outlier_detection(self, df: pd.DataFrame, 
                                       columns: List[str],
                                       eps: float = 0.5,
                                       min_samples: int = 5) -> Tuple[pd.DataFrame, Dict]:
        """
        Detect outliers using DBSCAN clustering
        
        Args:
            df: DataFrame
            columns: Columns to use for clustering
            eps: DBSCAN epsilon parameter
            min_samples: Minimum samples in a cluster
        
        Returns:
            Tuple[pd.DataFrame, Dict]: DataFrame with cluster labels and results
        """
        numeric_cols = [col for col in columns if col in df.select_dtypes(include=[np.number]).columns]
        
        if not numeric_cols:
            return df, {'message': 'No numeric columns found for clustering'}
        
        # Prepare data
        X = df[numeric_cols].copy()
        X = X.fillna(X.mean())
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply DBSCAN
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        cluster_labels = dbscan.fit_predict(X_scaled)
        
        # Create result DataFrame
        result_df = df.copy()
        result_df['cluster_label'] = cluster_labels
        
        outlier_count = (cluster_labels == -1).sum()
        n_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)
        
        return result_df, {
            'total_outliers': int(outlier_count),
            'outlier_percentage': float(outlier_count / len(df) * 100),
            'n_clusters': n_clusters,
            'analyzed_columns': numeric_cols
        }
    
    def generate_smart_suggestions(self, df: pd.DataFrame) -> List[Dict]:
        """
        Generate intelligent suggestions for data cleaning
        
        Args:
            df: DataFrame to analyze
        
        Returns:
            List[Dict]: List of suggestions with priorities
        """
        suggestions = []
        
        # Check for missing values
        missing_counts = df.isnull().sum()
        cols_with_missing = missing_counts[missing_counts > 0]
        
        if len(cols_with_missing) > 0:
            for col in cols_with_missing.index:
                missing_pct = missing_counts[col] / len(df) * 100
                if missing_pct > 50:
                    suggestions.append({
                        'priority': 'High',
                        'type': 'Missing Values',
                        'column': col,
                        'issue': f'{missing_pct:.1f}% missing values',
                        'suggestion': f'Consider dropping column {col} or using advanced imputation',
                        'action': 'drop_column_or_impute'
                    })
                elif missing_pct > 20:
                    suggestions.append({
                        'priority': 'Medium',
                        'type': 'Missing Values',
                        'column': col,
                        'issue': f'{missing_pct:.1f}% missing values',
                        'suggestion': f'Use KNN or iterative imputation for {col}',
                        'action': 'advanced_impute'
                    })
                else:
                    suggestions.append({
                        'priority': 'Low',
                        'type': 'Missing Values',
                        'column': col,
                        'issue': f'{missing_pct:.1f}% missing values',
                        'suggestion': f'Use mean/median imputation for {col}',
                        'action': 'simple_impute'
                    })
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            suggestions.append({
                'priority': 'High' if duplicates > len(df) * 0.05 else 'Medium',
                'type': 'Duplicates',
                'column': 'All',
                'issue': f'{duplicates} duplicate rows found',
                'suggestion': 'Remove duplicate rows',
                'action': 'remove_duplicates'
            })
        
        # Check for high cardinality categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            unique_count = df[col].nunique()
            if unique_count > len(df) * 0.5:
                suggestions.append({
                    'priority': 'Medium',
                    'type': 'High Cardinality',
                    'column': col,
                    'issue': f'{unique_count} unique values ({unique_count/len(df)*100:.1f}% of rows)',
                    'suggestion': f'Consider feature hashing or target encoding for {col}',
                    'action': 'encode_high_cardinality'
                })
        
        # Check for constant or near-constant columns
        for col in df.columns:
            if df[col].nunique() == 1:
                suggestions.append({
                    'priority': 'High',
                    'type': 'Constant Column',
                    'column': col,
                    'issue': 'Column has only one unique value',
                    'suggestion': f'Consider dropping {col} as it provides no information',
                    'action': 'drop_column'
                })
            elif df[col].nunique() < 3 and len(df) > 100:
                value_counts = df[col].value_counts()
                if value_counts.iloc[0] / len(df) > 0.95:
                    suggestions.append({
                        'priority': 'Medium',
                        'type': 'Near-Constant Column',
                        'column': col,
                        'issue': f'95%+ of values are the same',
                        'suggestion': f'Consider dropping {col} or investigating rare values',
                        'action': 'investigate_or_drop'
                    })
        
        # Check for potential outliers in numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
            
            if outliers > 0:
                outlier_pct = outliers / len(df) * 100
                if outlier_pct > 5:
                    suggestions.append({
                        'priority': 'Medium',
                        'type': 'Outliers',
                        'column': col,
                        'issue': f'{outliers} potential outliers ({outlier_pct:.1f}%)',
                        'suggestion': f'Review and handle outliers in {col} using IQR or Isolation Forest',
                        'action': 'handle_outliers'
                    })
        
        # Check for text formatting issues
        for col in categorical_cols:
            col_data = df[col].dropna().astype(str)
            if len(col_data) > 0:
                # Check for mixed case
                if col_data.str.lower().nunique() < col_data.nunique():
                    suggestions.append({
                        'priority': 'Low',
                        'type': 'Text Formatting',
                        'column': col,
                        'issue': 'Mixed case variations detected',
                        'suggestion': f'Standardize text case in {col}',
                        'action': 'standardize_case'
                    })
                
                # Check for whitespace issues
                if col_data.str.strip().nunique() < col_data.nunique():
                    suggestions.append({
                        'priority': 'Low',
                        'type': 'Text Formatting',
                        'column': col,
                        'issue': 'Leading/trailing whitespace detected',
                        'suggestion': f'Strip whitespace from {col}',
                        'action': 'strip_whitespace'
                    })
        
        # Sort by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        suggestions.sort(key=lambda x: priority_order[x['priority']])
        
        return suggestions
    
    def auto_fix_suggestions(self, df: pd.DataFrame, suggestion: Dict) -> pd.DataFrame:
        """
        Automatically apply a suggested fix
        
        Args:
            df: DataFrame
            suggestion: Suggestion dictionary
        
        Returns:
            pd.DataFrame: Fixed DataFrame
        """
        fixed_df = df.copy()
        action = suggestion.get('action')
        column = suggestion.get('column')
        
        try:
            if action == 'drop_column' and column != 'All':
                fixed_df = fixed_df.drop(columns=[column])
            
            elif action == 'remove_duplicates':
                fixed_df = fixed_df.drop_duplicates()
            
            elif action == 'simple_impute' and column != 'All':
                if fixed_df[column].dtype in [np.float64, np.int64]:
                    median_val = fixed_df[column].median()
                    fixed_df[column] = fixed_df[column].fillna(median_val)
                else:
                    mode_series = fixed_df[column].mode()
                    mode_val = mode_series.iloc[0] if len(mode_series) > 0 else ''
                    fixed_df[column] = fixed_df[column].fillna(mode_val)
            
            elif action == 'strip_whitespace' and column != 'All':
                if fixed_df[column].dtype == 'object':
                    fixed_df[column] = fixed_df[column].str.strip()
            
            elif action == 'standardize_case' and column != 'All':
                if fixed_df[column].dtype == 'object':
                    fixed_df[column] = fixed_df[column].str.lower()
            
        except Exception as e:
            print(f"Error applying fix: {str(e)}")
            return df
        
        return fixed_df
    
    def dimensionality_analysis(self, df: pd.DataFrame, 
                               n_components: int = 2) -> Tuple[pd.DataFrame, Dict]:
        """
        Analyze data dimensionality using PCA
        
        Args:
            df: DataFrame
            n_components: Number of principal components
        
        Returns:
            Tuple[pd.DataFrame, Dict]: Transformed data and analysis results
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) < 2:
            return df, {'message': 'Need at least 2 numeric columns for PCA'}
        
        # Prepare data
        X = df[numeric_cols].copy()
        X = X.fillna(X.mean())
        X_scaled = self.scaler.fit_transform(X)
        
        # Apply PCA
        n_components = min(n_components, len(numeric_cols))
        pca = PCA(n_components=n_components)
        X_pca = pca.fit_transform(X_scaled)
        
        # Create result DataFrame
        pc_columns = [f'PC{i+1}' for i in range(n_components)]
        result_df = pd.DataFrame(X_pca, columns=pc_columns)  # type: ignore
        
        return result_df, {
            'explained_variance_ratio': pca.explained_variance_ratio_.tolist(),
            'cumulative_variance': np.cumsum(pca.explained_variance_ratio_).tolist(),
            'n_components': n_components,
            'original_features': numeric_cols
        }
