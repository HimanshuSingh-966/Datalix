"""
Data cleaning operations
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from sklearn.ensemble import IsolationForest
import re


class DataCleaner:
    """Perform various data cleaning operations"""
    
    def auto_clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Perform automated cleaning workflow
        
        Args:
            df: DataFrame to clean
        
        Returns:
            Tuple[pd.DataFrame, List[str]]: Cleaned dataframe and list of operations
        """
        operations = []
        cleaned_df = df.copy()
        
        # Remove duplicates
        duplicates_before = cleaned_df.duplicated().sum()
        if duplicates_before > 0:
            cleaned_df = cleaned_df.drop_duplicates()
            operations.append(f"Removed {duplicates_before} duplicate rows")
        
        # Remove columns with >95% missing values
        missing_threshold = 0.95
        cols_to_drop = []
        for col in cleaned_df.columns:
            missing_pct = cleaned_df[col].isnull().sum() / len(cleaned_df)
            if missing_pct > missing_threshold:
                cols_to_drop.append(col)
        
        if cols_to_drop:
            cleaned_df = cleaned_df.drop(columns=cols_to_drop)
            operations.append(f"Removed {len(cols_to_drop)} columns with >95% missing values")
        
        # Clean text columns
        text_cols = cleaned_df.select_dtypes(include=['object']).columns
        for col in text_cols:
            # Strip whitespace
            cleaned_df[col] = cleaned_df[col].str.strip()
            # Remove extra spaces
            cleaned_df[col] = cleaned_df[col].str.replace(r'\s+', ' ', regex=True)
        
        if len(text_cols) > 0:
            operations.append(f"Cleaned {len(text_cols)} text columns (whitespace normalization)")
        
        # Convert appropriate columns to datetime
        for col in cleaned_df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    cleaned_df[col] = pd.to_datetime(cleaned_df[col], errors='coerce')
                    operations.append(f"Converted {col} to datetime")
                except:
                    pass
        
        return cleaned_df, operations
    
    def clean_text_columns(self, df: pd.DataFrame, columns: List[str], 
                          operations: Dict[str, bool]) -> pd.DataFrame:
        """
        Clean text columns based on specified operations
        
        Args:
            df: DataFrame
            columns: Columns to clean
            operations: Dictionary of operations to perform
        
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        cleaned_df = df.copy()
        
        for col in columns:
            if operations.get("Remove extra whitespace"):
                cleaned_df[col] = cleaned_df[col].str.replace(r'\s+', ' ', regex=True)
            
            if operations.get("Convert to lowercase"):
                cleaned_df[col] = cleaned_df[col].str.lower()
            
            if operations.get("Remove special characters"):
                cleaned_df[col] = cleaned_df[col].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
            
            if operations.get("Remove numbers"):
                cleaned_df[col] = cleaned_df[col].str.replace(r'\d+', '', regex=True)
            
            if operations.get("Strip whitespace"):
                cleaned_df[col] = cleaned_df[col].str.strip()
        
        return cleaned_df
    
    def detect_outliers(self, df: pd.DataFrame, column: str, 
                       method: str = 'iqr', **kwargs) -> pd.Series:
        """
        Detect outliers in a column
        
        Args:
            df: DataFrame
            column: Column name
            method: Detection method ('iqr', 'zscore', 'isolation_forest')
            **kwargs: Method-specific parameters
        
        Returns:
            pd.Series: Boolean series indicating outliers
        """
        if method == 'iqr':
            threshold = kwargs.get('threshold', 1.5)
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outliers = (df[column] < lower_bound) | (df[column] > upper_bound)
        
        elif method == 'zscore':
            threshold = kwargs.get('threshold', 3.0)
            mean = df[column].mean()
            std = df[column].std()
            
            z_scores = np.abs((df[column] - mean) / std)
            outliers = z_scores > threshold
        
        elif method == 'isolation_forest':
            contamination = kwargs.get('contamination', 0.1)
            
            # Prepare data
            X = df[[column]].fillna(df[column].median())
            
            # Fit Isolation Forest
            clf = IsolationForest(contamination=contamination, random_state=42)
            predictions = clf.fit_predict(X)
            
            # -1 indicates outlier
            outliers = pd.Series(predictions == -1, index=df.index)
        
        else:
            raise ValueError(f"Unknown outlier detection method: {method}")
        
        return outliers
