"""
Advanced Dashboard Builder with Drag-and-Drop Widgets
Create custom, shareable reports with interactive widgets
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Optional, Any
import json
import uuid
from datetime import datetime


class DashboardWidget:
    """Represents a single dashboard widget"""
    
    def __init__(self, widget_id: str, widget_type: str, title: str, config: Dict):
        self.widget_id = widget_id
        self.widget_type = widget_type
        self.title = title
        self.config = config
        self.position = {'row': 0, 'col': 0}
        self.size = {'width': 1, 'height': 1}
    
    def to_dict(self) -> Dict:
        """Convert widget to dictionary"""
        return {
            'widget_id': self.widget_id,
            'widget_type': self.widget_type,
            'title': self.title,
            'config': self.config,
            'position': self.position,
            'size': self.size
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DashboardWidget':
        """Create widget from dictionary"""
        widget = cls(
            data['widget_id'],
            data['widget_type'],
            data['title'],
            data['config']
        )
        widget.position = data.get('position', {'row': 0, 'col': 0})
        widget.size = data.get('size', {'width': 1, 'height': 1})
        return widget


class Dashboard:
    """Represents a custom dashboard"""
    
    def __init__(self, dashboard_id: str, name: str, description: str = ""):
        self.dashboard_id = dashboard_id
        self.name = name
        self.description = description
        self.widgets: List[DashboardWidget] = []
        self.layout = {'rows': 2, 'cols': 2}
        self.theme = 'plotly_dark'
        self.created = datetime.now().isoformat()
        self.last_modified = datetime.now().isoformat()
    
    def add_widget(self, widget_type: str, title: str, config: Dict,
                   row: int = 0, col: int = 0) -> DashboardWidget:
        """Add a widget to the dashboard"""
        widget_id = str(uuid.uuid4())
        widget = DashboardWidget(widget_id, widget_type, title, config)
        widget.position = {'row': row, 'col': col}
        self.widgets.append(widget)
        self.last_modified = datetime.now().isoformat()
        return widget
    
    def remove_widget(self, widget_id: str) -> bool:
        """Remove a widget from the dashboard"""
        for i, widget in enumerate(self.widgets):
            if widget.widget_id == widget_id:
                self.widgets.pop(i)
                self.last_modified = datetime.now().isoformat()
                return True
        return False
    
    def update_widget_position(self, widget_id: str, row: int, col: int):
        """Update widget position"""
        for widget in self.widgets:
            if widget.widget_id == widget_id:
                widget.position = {'row': row, 'col': col}
                self.last_modified = datetime.now().isoformat()
                return True
        return False
    
    def set_layout(self, rows: int, cols: int):
        """Set dashboard layout"""
        self.layout = {'rows': rows, 'cols': cols}
        self.last_modified = datetime.now().isoformat()
    
    def render(self, df: pd.DataFrame) -> go.Figure:
        """
        Render the dashboard with data
        
        Args:
            df: DataFrame containing the data
        
        Returns:
            go.Figure: Plotly figure with all widgets
        """
        from visualization.charts import ChartGenerator
        
        chart_gen = ChartGenerator()
        rows = self.layout['rows']
        cols = self.layout['cols']
        
        # Create subplots
        subplot_titles = []
        for widget in self.widgets[:rows * cols]:
            subplot_titles.append(widget.title)
        
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=subplot_titles,
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # Add widgets to subplots
        for i, widget in enumerate(self.widgets[:rows * cols]):
            row = (i // cols) + 1
            col = (i % cols) + 1
            
            try:
                widget_fig = self._create_widget_figure(widget, df, chart_gen)
                if widget_fig and widget_fig.data:
                    for trace in widget_fig.data:
                        fig.add_trace(trace, row=row, col=col)
            except Exception as e:
                print(f"Error rendering widget {widget.title}: {str(e)}")
        
        # Update layout
        fig.update_layout(
            height=400 * rows,
            showlegend=True,
            template=self.theme,
            title_text=self.name
        )
        
        return fig
    
    def _create_widget_figure(self, widget: DashboardWidget, df: pd.DataFrame,
                             chart_gen) -> Optional[go.Figure]:
        """Create a figure for a specific widget"""
        widget_type = widget.widget_type
        config = widget.config
        
        try:
            if widget_type == 'histogram':
                column = config.get('column')
                if column and column in df.columns:
                    return chart_gen.create_histogram(df, column, config.get('bins', 30))
            
            elif widget_type == 'box_plot':
                column = config.get('column')
                group_by = config.get('group_by')
                if column and column in df.columns:
                    return chart_gen.create_boxplot(df, column, group_by)
            
            elif widget_type == 'scatter':
                x_col = config.get('x_column')
                y_col = config.get('y_column')
                color_by = config.get('color_by')
                if x_col and y_col and x_col in df.columns and y_col in df.columns:
                    return chart_gen.create_scatter(df, x_col, y_col, color_by)
            
            elif widget_type == 'line_chart':
                y_cols = config.get('y_columns', [])
                x_col = config.get('x_column')
                valid_cols = [col for col in y_cols if col in df.columns]
                if valid_cols:
                    return chart_gen.create_line_chart(df, valid_cols, x_col)
            
            elif widget_type == 'bar_chart':
                x_col = config.get('x_column')
                y_col = config.get('y_column')
                if x_col and y_col and x_col in df.columns and y_col in df.columns:
                    return chart_gen.create_bar_chart(df, x_col, y_col)
            
            elif widget_type == 'heatmap':
                columns = config.get('columns', [])
                valid_cols = [col for col in columns if col in df.columns]
                if valid_cols:
                    return chart_gen.create_heatmap(df[valid_cols])
            
            elif widget_type == 'metric':
                column = config.get('column')
                aggregation = config.get('aggregation', 'mean')
                if column and column in df.columns:
                    if aggregation == 'mean':
                        value = df[column].mean()
                    elif aggregation == 'sum':
                        value = df[column].sum()
                    elif aggregation == 'count':
                        value = df[column].count()
                    elif aggregation == 'max':
                        value = df[column].max()
                    elif aggregation == 'min':
                        value = df[column].min()
                    else:
                        value = df[column].mean()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Indicator(
                        mode="number+delta",
                        value=value,
                        title={'text': f"{column} ({aggregation})"},
                    ))
                    return fig
            
            elif widget_type == 'table':
                columns = config.get('columns', df.columns.tolist())
                limit = config.get('limit', 10)
                valid_cols = [col for col in columns if col in df.columns]
                
                if valid_cols:
                    table_df = df[valid_cols].head(limit)
                    fig = go.Figure(data=[go.Table(
                        header=dict(values=list(table_df.columns),
                                  fill_color='paleturquoise',
                                  align='left'),
                        cells=dict(values=[table_df[col] for col in table_df.columns],
                                 fill_color='lavender',
                                 align='left'))
                    ])
                    return fig
        
        except Exception as e:
            print(f"Error creating widget figure: {str(e)}")
        
        return None
    
    def to_dict(self) -> Dict:
        """Convert dashboard to dictionary"""
        return {
            'dashboard_id': self.dashboard_id,
            'name': self.name,
            'description': self.description,
            'widgets': [widget.to_dict() for widget in self.widgets],
            'layout': self.layout,
            'theme': self.theme,
            'created': self.created,
            'last_modified': self.last_modified
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Dashboard':
        """Create dashboard from dictionary"""
        dashboard = cls(
            data['dashboard_id'],
            data['name'],
            data.get('description', '')
        )
        dashboard.widgets = [DashboardWidget.from_dict(w) for w in data.get('widgets', [])]
        dashboard.layout = data.get('layout', {'rows': 2, 'cols': 2})
        dashboard.theme = data.get('theme', 'plotly_dark')
        dashboard.created = data.get('created', datetime.now().isoformat())
        dashboard.last_modified = data.get('last_modified', datetime.now().isoformat())
        return dashboard
    
    def export_html(self, df: pd.DataFrame, filepath: str) -> bool:
        """Export dashboard as standalone HTML file"""
        try:
            fig = self.render(df)
            fig.write_html(filepath)
            return True
        except Exception as e:
            print(f"Error exporting dashboard: {str(e)}")
            return False


class DashboardManager:
    """Manage multiple dashboards"""
    
    def __init__(self):
        self.dashboards: Dict[str, Dashboard] = {}
    
    def create_dashboard(self, name: str, description: str = "") -> Dashboard:
        """Create a new dashboard"""
        dashboard_id = str(uuid.uuid4())
        dashboard = Dashboard(dashboard_id, name, description)
        self.dashboards[dashboard_id] = dashboard
        return dashboard
    
    def delete_dashboard(self, dashboard_id: str) -> bool:
        """Delete a dashboard"""
        if dashboard_id in self.dashboards:
            del self.dashboards[dashboard_id]
            return True
        return False
    
    def get_dashboard(self, dashboard_id: str) -> Optional[Dashboard]:
        """Get a dashboard by ID"""
        return self.dashboards.get(dashboard_id)
    
    def list_dashboards(self) -> List[Dict]:
        """List all dashboards"""
        return [
            {
                'dashboard_id': d.dashboard_id,
                'name': d.name,
                'description': d.description,
                'widgets_count': len(d.widgets),
                'created': d.created,
                'last_modified': d.last_modified
            }
            for d in self.dashboards.values()
        ]
    
    def save_dashboard(self, dashboard: Dashboard, filepath: str) -> bool:
        """Save dashboard to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(dashboard.to_dict(), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving dashboard: {str(e)}")
            return False
    
    def load_dashboard(self, filepath: str) -> Optional[Dashboard]:
        """Load dashboard from file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            dashboard = Dashboard.from_dict(data)
            self.dashboards[dashboard.dashboard_id] = dashboard
            return dashboard
        except Exception as e:
            print(f"Error loading dashboard: {str(e)}")
            return None
    
    def get_widget_templates(self) -> Dict[str, Dict]:
        """Get available widget templates"""
        return {
            'histogram': {
                'name': 'Histogram',
                'description': 'Show distribution of a numeric column',
                'required_config': ['column'],
                'optional_config': ['bins']
            },
            'box_plot': {
                'name': 'Box Plot',
                'description': 'Show statistical summary with outliers',
                'required_config': ['column'],
                'optional_config': ['group_by']
            },
            'scatter': {
                'name': 'Scatter Plot',
                'description': 'Show relationship between two variables',
                'required_config': ['x_column', 'y_column'],
                'optional_config': ['color_by']
            },
            'line_chart': {
                'name': 'Line Chart',
                'description': 'Show trends over time or sequence',
                'required_config': ['y_columns'],
                'optional_config': ['x_column']
            },
            'bar_chart': {
                'name': 'Bar Chart',
                'description': 'Compare categorical data',
                'required_config': ['x_column', 'y_column'],
                'optional_config': []
            },
            'heatmap': {
                'name': 'Heatmap',
                'description': 'Show correlation matrix',
                'required_config': ['columns'],
                'optional_config': []
            },
            'metric': {
                'name': 'Metric',
                'description': 'Display a single key metric',
                'required_config': ['column', 'aggregation'],
                'optional_config': []
            },
            'table': {
                'name': 'Table',
                'description': 'Show data in tabular format',
                'required_config': [],
                'optional_config': ['columns', 'limit']
            }
        }
