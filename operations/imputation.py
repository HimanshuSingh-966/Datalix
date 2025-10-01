"""
Missing value imputation operations
"""

import pandas as pd
import numpy as np
from typing import Optional, Union
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler


class MissingValueImputer:
    """Handle missing value imputation"""
    
    def __init__(self):
        self.imputers = {}
    
    def impute_column(self, df: pd.DataFrame, column: str, 
                     method: str, **kwargs) -> pd.DataFrame:
        """
        Impute missing values in a column
        
        Args:
            df: DataFrame
            column: Column to impute
            method: Imputation method
            **kwargs: Method-specific parameters
        
        Returns:
            pd.DataFrame: DataFrame with imputed values
        """
        imputed_df = df.copy()
        
        if method == "Mean":
            imputed_df[column] = imputed_df[column].fillna(imputed_df[column].mean())
        
        elif method == "Median":
            imputed_df[column] = imputed_df[column].fillna(imputed_df[column].median())
        
        elif method == "Mode":
            mode_value = imputed_df[column].mode()
            if len(mode_value) > 0:
                imputed_df[column] = imputed_df[column].fillna(mode_value[0])
        
        elif method == "Forward Fill":
            imputed_df[column] = imputed_df[column].fillna(method='ffill')
        
        elif method == "Backward Fill":
            imputed_df[column] = imputed_df[column].fillna(method='bfill')
        
        elif method == "KNN Imputation (ML)":
            n_neighbors = kwargs.get('n_neighbors', 5)
            
            # Use only numeric columns for KNN
            numeric_cols = imputed_df.select_dtypes(include=[np.number]).columns.tolist()
            
            if column in numeric_cols:
                # Prepare data
                X = imputed_df[numeric_cols].values
                
                # Fit and transform
                imputer = KNNImputer(n_neighbors=n_neighbors)
                X_imputed = imputer.fit_transform(X)
                
                # Update dataframe
                imputed_df[numeric_cols] = X_imputed
        
        elif method == "Interpolate":
            interpolation_method = kwargs.get('method', 'linear')
            order = kwargs.get('order', 2)
            
            if interpolation_method in ['polynomial', 'spline']:
                imputed_df[column] = imputed_df[column].interpolate(
                    method=interpolation_method,
                    order=order
                )
            else:
                imputed_df[column] = imputed_df[column].interpolate(
                    method=interpolation_method
                )
        
        elif method == "Constant Value":
            value = kwargs.get('value', 0)
            imputed_df[column] = imputed_df[column].fillna(value)
        
        return imputed_df
