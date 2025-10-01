"""
Data loading utilities with support for multiple formats and encoding detection
"""

import pandas as pd
import numpy as np
import io
from typing import Optional, Union, List
import chardet


class DataLoader:
    """Handle loading data from various sources and formats"""
    
    def __init__(self):
        self.supported_formats = ['csv', 'xlsx', 'xls', 'json', 'parquet', 'tsv', 'txt']
    
    def detect_separator(self, file_content: str, encoding: str = 'utf-8') -> str:
        """Detect the separator used in a CSV file"""
        # Try common separators
        separators = [',', ';', '\t', '|']
        max_cols = 0
        best_sep = ','
        
        for sep in separators:
            try:
                df = pd.read_csv(io.StringIO(file_content), sep=sep, nrows=5, encoding=encoding)
                if len(df.columns) > max_cols:
                    max_cols = len(df.columns)
                    best_sep = sep
            except:
                continue
        
        return best_sep
    
    def load_file(self, uploaded_file, encoding: str = 'utf-8', **kwargs) -> pd.DataFrame:
        """
        Load data from an uploaded file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            encoding: Character encoding to use
            **kwargs: Additional arguments to pass to pandas readers
        
        Returns:
            pd.DataFrame: Loaded data
        """
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Reset file pointer
        uploaded_file.seek(0)
        
        # Load based on format
        if file_extension in ['csv', 'tsv', 'txt']:
            # Read content for separator detection
            content = uploaded_file.read().decode(encoding, errors='replace')
            separator = self.detect_separator(content, encoding)
            
            # Read CSV with detected separator
            df = pd.read_csv(
                io.StringIO(content),
                sep=separator,
                encoding=encoding,
                low_memory=False,
                **kwargs
            )
        
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file, engine='openpyxl', **kwargs)
        
        elif file_extension == 'json':
            content = uploaded_file.read().decode(encoding)
            df = pd.read_json(io.StringIO(content), **kwargs)
        
        elif file_extension == 'parquet':
            df = pd.read_parquet(uploaded_file, **kwargs)
        
        else:
            raise ValueError(f"Handler not implemented for {file_extension}")
        
        return df
    
    def load_from_url(self, url: str, **kwargs) -> pd.DataFrame:
        """
        Load data from a URL
        
        Args:
            url: URL to load data from
            **kwargs: Additional arguments
        
        Returns:
            pd.DataFrame: Loaded data
        """
        # Determine format from URL
        if url.endswith('.csv'):
            df = pd.read_csv(url, **kwargs)
        elif url.endswith('.json'):
            df = pd.read_json(url, **kwargs)
        elif url.endswith('.parquet'):
            df = pd.read_parquet(url, **kwargs)
        else:
            # Try CSV by default
            df = pd.read_csv(url, **kwargs)
        
        return df
    
    def load_sample_data(self, dataset_name: str) -> pd.DataFrame:
        """
        Load sample datasets for testing
        
        Args:
            dataset_name: Name of the sample dataset
        
        Returns:
            pd.DataFrame: Sample data
        """
        np.random.seed(42)
        
        if dataset_name == "Sales Data":
            # Create sample sales data
            n_rows = 1000
            dates = pd.date_range(start='2023-01-01', periods=n_rows, freq='D')
            
            df = pd.DataFrame({
                'date': dates,
                'product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], n_rows),
                'revenue': np.random.lognormal(5, 1, n_rows).round(2),
                'quantity': np.random.poisson(10, n_rows),
                'customer_segment': np.random.choice(['Retail', 'Wholesale', 'Online'], n_rows),
                'region': np.random.choice(['North', 'South', 'East', 'West'], n_rows)
            })
            
            # Add some missing values
            df.loc[np.random.choice(df.index, 50), 'revenue'] = np.nan
            df.loc[np.random.choice(df.index, 30), 'quantity'] = np.nan
            
            # Add some outliers
            outlier_idx = np.random.choice(df.index, 20)
            df.loc[outlier_idx, 'revenue'] = df.loc[outlier_idx, 'revenue'] * 10
        
        elif dataset_name == "Customer Data":
            # Create sample customer data
            n_rows = 500
            
            df = pd.DataFrame({
                'customer_id': range(1, n_rows + 1),
                'name': [f'Customer {i}' for i in range(1, n_rows + 1)],
                'email': [f'customer{i}@example.com' if i % 10 != 0 else None for i in range(1, n_rows + 1)],
                'age': np.random.randint(18, 80, n_rows),
                'city': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], n_rows),
                'signup_date': pd.date_range(start='2020-01-01', periods=n_rows, freq='D'),
                'total_purchases': np.random.poisson(5, n_rows),
                'total_spent': np.random.lognormal(6, 1, n_rows).round(2)
            })
            
            # Add missing values
            df.loc[np.random.choice(df.index, 30), 'age'] = np.nan
            df.loc[np.random.choice(df.index, 20), 'city'] = np.nan
        
        elif dataset_name == "Financial Data":
            # Create sample stock data
            n_rows = 252  # Trading days in a year
            dates = pd.date_range(start='2023-01-01', periods=n_rows, freq='B')
            
            # Simulate stock prices
            initial_price = 100
            returns = np.random.normal(0.001, 0.02, n_rows)
            prices = initial_price * np.exp(np.cumsum(returns))
            
            df = pd.DataFrame({
                'date': dates,
                'open': prices * (1 + np.random.normal(0, 0.01, n_rows)),
                'high': prices * (1 + np.abs(np.random.normal(0.01, 0.01, n_rows))),
                'low': prices * (1 - np.abs(np.random.normal(0.01, 0.01, n_rows))),
                'close': prices,
                'volume': np.random.lognormal(15, 1, n_rows).astype(int),
                'returns': returns
            })
            
            # Round prices
            for col in ['open', 'high', 'low', 'close']:
                df[col] = df[col].round(2)
        
        else:
            raise ValueError(f"Unknown sample dataset: {dataset_name}")
        
        return df
    
    def chunk_load_large_file(self, uploaded_file, encoding: str = 'utf-8', 
                             chunksize: int = 10000) -> pd.DataFrame:
        """
        Load large files in chunks to avoid memory issues
        
        Args:
            uploaded_file: Streamlit uploaded file object
            encoding: Character encoding
            chunksize: Number of rows per chunk
        
        Returns:
            pd.DataFrame: Loaded data
        """
        chunks = []
        
        for chunk in pd.read_csv(uploaded_file, encoding=encoding, chunksize=chunksize):
            chunks.append(chunk)
        
        return pd.concat(chunks, ignore_index=True)
