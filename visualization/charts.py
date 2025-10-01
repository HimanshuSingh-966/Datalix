"""
Chart generation utilities using Plotly
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Optional, List


class ChartGenerator:
    """Generate interactive charts using Plotly"""
    
    def create_histogram(self, df: pd.DataFrame, column: str, 
                        bins: int = 30) -> go.Figure:
        """Create histogram"""
        fig = px.histogram(
            df,
            x=column,
            nbins=bins,
            title=f"Distribution of {column}",
            labels={column: column, 'count': 'Frequency'}
        )
        
        fig.update_layout(
            showlegend=False,
            hovermode='x unified'
        )
        
        return fig
    
    def create_boxplot(self, df: pd.DataFrame, column: str, 
                      group_by: Optional[str] = None) -> go.Figure:
        """Create box plot"""
        if group_by:
            fig = px.box(
                df,
                x=group_by,
                y=column,
                title=f"Box Plot of {column} by {group_by}",
                color=group_by
            )
        else:
            fig = px.box(
                df,
                y=column,
                title=f"Box Plot of {column}"
            )
        
        fig.update_layout(showlegend=True if group_by else False)
        
        return fig
    
    def create_scatter(self, df: pd.DataFrame, x_col: str, y_col: str,
                      color_by: Optional[str] = None) -> go.Figure:
        """Create scatter plot"""
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_by,
            title=f"{y_col} vs {x_col}",
            labels={x_col: x_col, y_col: y_col},
            hover_data=df.columns[:5].tolist()  # Show first 5 columns on hover
        )
        
        # Add trendline
        if color_by is None:
            fig.add_traces(
                px.scatter(df, x=x_col, y=y_col, trendline="ols").data[1]
            )
        
        return fig
    
    def create_line_chart(self, df: pd.DataFrame, y_cols: List[str],
                         x_col: Optional[str] = None) -> go.Figure:
        """Create line chart"""
        fig = go.Figure()
        
        x_data = df[x_col] if x_col else df.index
        
        for col in y_cols:
            fig.add_trace(go.Scatter(
                x=x_data,
                y=df[col],
                mode='lines',
                name=col
            ))
        
        fig.update_layout(
            title="Line Chart",
            xaxis_title=x_col if x_col else "Index",
            yaxis_title="Value",
            hovermode='x unified'
        )
        
        return fig
    
    def create_bar_chart(self, df: pd.DataFrame, x_col: str,
                        y_col: Optional[str] = None,
                        agg_func: str = 'count') -> go.Figure:
        """Create bar chart"""
        if agg_func == 'count':
            # Count occurrences
            data = df[x_col].value_counts().sort_index()
            fig = px.bar(
                x=data.index,
                y=data.values,
                title=f"Count by {x_col}",
                labels={'x': x_col, 'y': 'Count'}
            )
        else:
            # Aggregate by function
            if y_col:
                if agg_func == 'sum':
                    data = df.groupby(x_col)[y_col].sum()
                elif agg_func == 'mean':
                    data = df.groupby(x_col)[y_col].mean()
                elif agg_func == 'median':
                    data = df.groupby(x_col)[y_col].median()
                
                fig = px.bar(
                    x=data.index,
                    y=data.values,
                    title=f"{agg_func.title()} of {y_col} by {x_col}",
                    labels={'x': x_col, 'y': f"{agg_func.title()} of {y_col}"}
                )
        
        fig.update_layout(showlegend=False)
        
        return fig
    
    def create_correlation_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Create correlation heatmap"""
        # Calculate correlation
        corr = df.corr()
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Correlation Heatmap",
            width=800,
            height=800
        )
        
        return fig
    
    def create_distribution_plot(self, df: pd.DataFrame, column: str) -> go.Figure:
        """Create distribution plot with histogram and KDE"""
        fig = make_subplots(rows=2, cols=1, 
                           subplot_titles=("Histogram", "Box Plot"),
                           vertical_spacing=0.15)
        
        # Histogram
        fig.add_trace(
            go.Histogram(x=df[column], name="Distribution", nbinsx=30),
            row=1, col=1
        )
        
        # Box plot
        fig.add_trace(
            go.Box(x=df[column], name="Box Plot"),
            row=2, col=1
        )
        
        fig.update_layout(
            title=f"Distribution Analysis: {column}",
            showlegend=False,
            height=600
        )
        
        return fig
    
    def create_pair_plot(self, df: pd.DataFrame) -> go.Figure:
        """Create pair plot (scatter matrix)"""
        fig = px.scatter_matrix(
            df,
            dimensions=df.columns.tolist(),
            title="Pair Plot (Scatter Matrix)"
        )
        
        fig.update_traces(diagonal_visible=False, showupperhalf=False)
        
        return fig
