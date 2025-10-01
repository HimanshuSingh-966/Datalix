"""
Operation history tracking with undo capability
"""

import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime


class HistoryTracker:
    """Track data cleaning operations for undo functionality"""
    
    def __init__(self):
        self.history: List[Dict] = []
        self.max_history = 50  # Keep last 50 operations
    
    def add_operation(self, operation: str, data_snapshot: pd.DataFrame):
        """
        Add an operation to history
        
        Args:
            operation: Description of the operation
            data_snapshot: DataFrame snapshot before operation
        """
        self.history.append({
            'operation': operation,
            'data': data_snapshot.copy(),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
    
    def undo(self) -> Optional[pd.DataFrame]:
        """
        Undo last operation
        
        Returns:
            Optional[pd.DataFrame]: Previous data state or None
        """
        if self.history:
            last_state = self.history.pop()
            return last_state['data']
        return None
    
    def get_history(self) -> List[Dict]:
        """Get operation history"""
        return [
            {
                'operation': item['operation'],
                'timestamp': item['timestamp']
            }
            for item in self.history
        ]
    
    def clear(self):
        """Clear history"""
        self.history = []
