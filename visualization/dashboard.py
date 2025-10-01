"""
Dashboard building utilities
"""

import pandas as pd
from typing import List, Dict
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class DashboardBuilder:
    """Build custom dashboards with multiple charts"""
    
    def __init__(self):
        self.layouts = {
            '2x2': (2, 2),
            'single_row': (1, 4),
            'single_column': (4, 1)
        }
    
    def create_dashboard(self, charts: List[go.Figure], 
                        layout: str = '2x2') -> go.Figure:
        """
        Create a dashboard with multiple charts
        
        Args:
            charts: List of Plotly figures
            layout: Layout type
        
        Returns:
            go.Figure: Combined dashboard figure
        """
        rows, cols = self.layouts.get(layout, (2, 2))
        
        # Create subplots
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=[f"Chart {i+1}" for i in range(len(charts))]
        )
        
        # Add charts
        for i, chart in enumerate(charts):
            row = (i // cols) + 1
            col = (i % cols) + 1
            
            for trace in chart.data:
                fig.add_trace(trace, row=row, col=col)
        
        fig.update_layout(
            height=300 * rows,
            showlegend=True,
            title_text="Custom Dashboard"
        )
        
        return fig
