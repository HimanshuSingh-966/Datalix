# Datalix - Advanced Data Cleaning Platform

A comprehensive Streamlit-based application for data cleaning, preprocessing, and transformation with advanced ML capabilities.

## Features

### Core Features
- **Data Upload & Preview**: Support for CSV, Excel, JSON, and Parquet formats
- **Data Profiling**: Comprehensive quality assessment with scoring
- **Data Cleaning**: Automated cleaning workflows with undo functionality
- **Missing Value Handling**: Multiple imputation methods including KNN
- **Outlier Detection**: IQR, Z-Score, and Isolation Forest methods
- **Categorical Encoding**: Label, One-Hot, and Ordinal encoding

### Advanced Features

#### 🗄️ Database Connectivity
- Direct import from PostgreSQL and MySQL databases
- Export cleaned data to database tables
- Custom SQL query support
- Table browsing and column inspection

#### 🤖 ML-Based Data Cleaning
- **Multivariate Anomaly Detection**: Using Isolation Forest
- **Smart Suggestions**: Intelligent recommendations for data cleaning
- **Pattern Analysis**: Detect inconsistencies in text data
- **Dimensionality Analysis**: PCA-based feature reduction
- **Cluster-Based Outlier Detection**: Using DBSCAN

#### 📦 Batch Processing
- Process multiple files simultaneously
- Apply cleaning templates to batches
- Predefined templates for common tasks
- Custom template creation and saving

#### 🔄 Workflow Pipelines
- Create reusable data transformation pipelines
- Chain multiple operations together
- Save and load workflow definitions
- Execution history and logging
- Predefined pipelines for common scenarios

#### 📊 Dashboard Builder
- Drag-and-drop widget system
- Multiple chart types (histogram, scatter, line, bar, heatmap, etc.)
- Custom layout configuration (rows and columns)
- Export dashboards as standalone HTML files
- Shareable dashboard configurations

### Visualization
- Interactive Plotly charts
- Histogram, Box Plot, Scatter Plot, Line Chart
- Correlation Heatmap, Distribution Plot, Pair Plot
- Custom dashboard creation

## Installation

### Requirements
- Python 3.10 or higher
- Dependencies listed in `pyproject.toml`

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Or use uv (recommended)
uv sync

# Run the application
streamlit run app.py --server.port 5000
```

## Usage

1. **Upload Data**: Start by uploading your data file or connecting to a database
2. **Explore**: Use Data Preview and Profiling to understand your data
3. **Clean**: Apply cleaning operations manually or use ML suggestions
4. **Transform**: Create workflows or use batch processing for multiple files
5. **Visualize**: Build custom dashboards to explore your data
6. **Export**: Download cleaned data or export to a database

## Configuration

The application uses a dark theme by default. Configuration is stored in `.streamlit/config.toml`:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "dark"
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
```

## Project Structure

```
.
├── app.py                          # Main application
├── core/
│   ├── session_manager.py         # Session state management
│   └── history_tracker.py         # Undo/redo functionality
├── operations/
│   ├── cleaning.py                # Basic cleaning operations
│   ├── encoding.py                # Categorical encoding
│   ├── imputation.py              # Missing value imputation
│   ├── ml_cleaning.py             # ML-based cleaning
│   ├── batch_processor.py         # Batch processing
│   └── workflow_pipeline.py       # Workflow management
├── utils/
│   ├── data_loader.py             # Data loading utilities
│   ├── quality_assessment.py     # Data quality metrics
│   ├── encoding_detector.py      # File encoding detection
│   └── database_connector.py     # Database connectivity
├── visualization/
│   ├── charts.py                  # Chart generation
│   ├── dashboard.py               # Basic dashboard
│   └── dashboard_builder_advanced.py  # Advanced dashboard builder
└── .streamlit/
    └── config.toml                # Streamlit configuration
```

## Technologies Used

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Plotly**: Interactive visualizations
- **Scikit-learn**: Machine learning algorithms
- **SQLAlchemy**: Database connectivity
- **psycopg2**: PostgreSQL adapter
- **PyMySQL**: MySQL adapter

## License

This project is part of a data cleaning platform designed for educational and professional use.

## Version

Current version: 2.0.0 - Enhanced Edition

## Support

For issues or questions, please refer to the Help section in the application.
