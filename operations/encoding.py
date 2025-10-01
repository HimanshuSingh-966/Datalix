"""
Categorical encoding operations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder


class CategoricalEncoder:
    """Handle categorical encoding operations"""
    
    def __init__(self):
        self.label_encoders = {}
        self.ordinal_encoders = {}
    
    def label_encode(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """
        Apply label encoding to a column
        
        Args:
            df: DataFrame
            column: Column to encode
        
        Returns:
            pd.DataFrame: DataFrame with encoded column
        """
        encoded_df = df.copy()
        
        # Create and fit label encoder
        le = LabelEncoder()
        
        # Handle NaN values
        mask = encoded_df[column].notna()
        encoded_df.loc[mask, column] = le.fit_transform(encoded_df.loc[mask, column])
        
        # Store encoder
        self.label_encoders[column] = le
        
        return encoded_df
    
    def onehot_encode(self, df: pd.DataFrame, columns: List[str], 
                     drop_first: bool = True) -> pd.DataFrame:
        """
        Apply one-hot encoding to columns
        
        Args:
            df: DataFrame
            columns: Columns to encode
            drop_first: Whether to drop first category
        
        Returns:
            pd.DataFrame: DataFrame with one-hot encoded columns
        """
        encoded_df = df.copy()
        
        # Apply one-hot encoding
        encoded_df = pd.get_dummies(
            encoded_df, 
            columns=columns, 
            drop_first=drop_first,
            prefix_sep='_'
        )
        
        return encoded_df
    
    def ordinal_encode(self, df: pd.DataFrame, column: str, 
                      mapping: Dict) -> pd.DataFrame:
        """
        Apply ordinal encoding with custom mapping
        
        Args:
            df: DataFrame
            column: Column to encode
            mapping: Dictionary mapping categories to numbers
        
        Returns:
            pd.DataFrame: DataFrame with encoded column
        """
        encoded_df = df.copy()
        
        # Apply mapping - Use lambda to satisfy type checker
        encoded_df[column] = encoded_df[column].apply(lambda x: mapping.get(x, x))
        
        return encoded_df
    
    def get_encoding_info(self, column: str, encoding_type: str) -> Dict:
        """
        Get information about encoding for a column
        
        Args:
            column: Column name
            encoding_type: Type of encoding ('label', 'ordinal')
        
        Returns:
            Dict: Encoding information
        """
        if encoding_type == 'label' and column in self.label_encoders:
            le = self.label_encoders[column]
            return {
                'classes': le.classes_.tolist(),
                'n_classes': len(le.classes_)
            }
        
        return {}
