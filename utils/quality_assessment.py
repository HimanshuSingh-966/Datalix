"""
Data quality assessment and scoring utilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


class QualityAssessor:
    """Assess data quality and provide recommendations"""
    
    def __init__(self):
        self.weights = {
            'completeness': 0.4,
            'consistency': 0.3,
            'uniqueness': 0.2,
            'validity': 0.1
        }
    
    def calculate_completeness_score(self, df: pd.DataFrame) -> float:
        """
        Calculate completeness score (percentage of non-missing values)
        
        Args:
            df: DataFrame to assess
        
        Returns:
            float: Completeness score (0-100)
        """
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        return completeness
    
    def calculate_consistency_score(self, df: pd.DataFrame) -> float:
        """
        Calculate consistency score based on data type uniformity
        
        Args:
            df: DataFrame to assess
        
        Returns:
            float: Consistency score (0-100)
        """
        consistency_scores = []
        
        for col in df.columns:
            # Check if column has consistent data type
            if df[col].dtype == 'object':
                # For text columns, check if values are consistently formatted
                unique_patterns = df[col].dropna().apply(lambda x: len(str(x))).nunique()
                # Lower variation in length = higher consistency
                score = max(0, 100 - (unique_patterns / len(df) * 100))
            else:
                # Numeric columns are considered consistent
                score = 100
            
            consistency_scores.append(score)
        
        return np.mean(consistency_scores) if consistency_scores else 100
    
    def calculate_uniqueness_score(self, df: pd.DataFrame) -> float:
        """
        Calculate uniqueness score (percentage of unique records)
        
        Args:
            df: DataFrame to assess
        
        Returns:
            float: Uniqueness score (0-100)
        """
        total_rows = len(df)
        duplicate_rows = df.duplicated().sum()
        uniqueness = ((total_rows - duplicate_rows) / total_rows) * 100
        return uniqueness
    
    def calculate_validity_score(self, df: pd.DataFrame) -> float:
        """
        Calculate validity score based on outliers in numeric columns
        
        Args:
            df: DataFrame to assess
        
        Returns:
            float: Validity score (0-100)
        """
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            return 100
        
        outlier_counts = []
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            outlier_counts.append(outliers)
        
        total_outliers = sum(outlier_counts)
        total_values = len(df) * len(numeric_cols)
        validity = ((total_values - total_outliers) / total_values) * 100
        
        return validity
    
    def calculate_quality_score(self, df: pd.DataFrame) -> Dict:
        """
        Calculate overall data quality score
        
        Args:
            df: DataFrame to assess
        
        Returns:
            Dict: Quality metrics and overall score
        """
        # Calculate individual scores
        completeness = self.calculate_completeness_score(df)
        consistency = self.calculate_consistency_score(df)
        uniqueness = self.calculate_uniqueness_score(df)
        validity = self.calculate_validity_score(df)
        
        # Calculate weighted overall score
        overall_score = (
            completeness * self.weights['completeness'] +
            consistency * self.weights['consistency'] +
            uniqueness * self.weights['uniqueness'] +
            validity * self.weights['validity']
        )
        
        # Determine grade
        if overall_score >= 90:
            grade = "Excellent"
        elif overall_score >= 80:
            grade = "Very Good"
        elif overall_score >= 70:
            grade = "Good"
        elif overall_score >= 60:
            grade = "Fair"
        else:
            grade = "Needs Improvement"
        
        # Generate recommendations
        recommendations = self.generate_recommendations(df, {
            'completeness': completeness,
            'consistency': consistency,
            'uniqueness': uniqueness,
            'validity': validity
        })
        
        return {
            'overall_score': overall_score,
            'completeness_score': completeness,
            'consistency_score': consistency,
            'uniqueness_score': uniqueness,
            'validity_score': validity,
            'grade': grade,
            'recommendations': recommendations
        }
    
    def generate_recommendations(self, df: pd.DataFrame, scores: Dict) -> List[str]:
        """
        Generate improvement recommendations based on scores
        
        Args:
            df: DataFrame
            scores: Dictionary of quality scores
        
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        # Completeness recommendations
        if scores['completeness'] < 90:
            missing_pct = 100 - scores['completeness']
            recommendations.append(
                f"Address missing values ({missing_pct:.1f}% of data). "
                "Consider imputation or removal strategies."
            )
        
        # Consistency recommendations
        if scores['consistency'] < 80:
            recommendations.append(
                "Improve data consistency by standardizing text formats "
                "and ensuring uniform data entry."
            )
        
        # Uniqueness recommendations
        if scores['uniqueness'] < 95:
            duplicates = df.duplicated().sum()
            recommendations.append(
                f"Remove {duplicates} duplicate records to improve data uniqueness."
            )
        
        # Validity recommendations
        if scores['validity'] < 90:
            recommendations.append(
                "Review outliers in numeric columns. Consider if they are "
                "valid data points or errors that should be corrected."
            )
        
        if not recommendations:
            recommendations.append(
                "Data quality is excellent! Consider advanced analytics "
                "or machine learning applications."
            )
        
        return recommendations
    
    def analyze_missing_values(self, df: pd.DataFrame) -> Dict:
        """
        Detailed analysis of missing values
        
        Args:
            df: DataFrame to analyze
        
        Returns:
            Dict: Missing value statistics
        """
        missing_counts = df.isnull().sum()
        total_missing = missing_counts.sum()
        total_cells = df.shape[0] * df.shape[1]
        
        return {
            'total_missing': int(total_missing),
            'missing_percentage': (total_missing / total_cells * 100),
            'columns_with_missing': int((missing_counts > 0).sum()),
            'missing_by_column': missing_counts[missing_counts > 0]
        }
