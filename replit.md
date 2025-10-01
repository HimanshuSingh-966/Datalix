# Datalix - Advanced Data Cleaning Platform

## Overview

Datalix is a comprehensive Streamlit-based data cleaning and preprocessing platform designed for automated data quality improvement. The application provides both traditional data cleaning operations and advanced ML-based cleaning capabilities, with support for multiple file formats, database connectivity, and reusable workflow pipelines.

The platform serves data analysts and data scientists who need to clean, transform, and analyze datasets before downstream processing. It features an interactive web interface built with Streamlit, allowing users to upload data, apply cleaning operations, visualize results, and export cleaned data to various destinations.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
**Framework**: Streamlit-based single-page application with multi-page navigation
- **Main Application**: `app.py` serves as the entry point with page configuration and module imports
- **Session Management**: Centralized session state management through `SessionManager` class for maintaining user data and application state across interactions
- **History Tracking**: Undo/redo functionality via `HistoryTracker` that maintains operation snapshots (limit: 50 operations)
- **UI Pattern**: Wide layout with expanded sidebar for navigation between functional modules

**Design Decision**: Streamlit was chosen for rapid development and built-in interactivity. The session-based architecture allows maintaining state without complex frontend frameworks, though it limits multi-user concurrent access to individual session scopes.

### Backend Architecture

#### Data Processing Layer
**Core Operations**:
- **Data Cleaning** (`operations/cleaning.py`): Auto-clean workflows including duplicate removal, missing value threshold filtering, and text normalization
- **Missing Value Imputation** (`operations/imputation.py`): Multiple strategies (mean, median, mode, forward/backward fill, KNN)
- **Categorical Encoding** (`operations/encoding.py`): Label encoding, one-hot encoding, and ordinal encoding with encoder persistence
- **ML-Based Cleaning** (`operations/ml_cleaning.py`): Isolation Forest for multivariate anomaly detection, smart cleaning suggestions, pattern analysis

**Design Decision**: Each operation module is independent and stateless, operating on DataFrame copies to preserve data integrity. Scikit-learn is used for ML operations due to its stability and comprehensive algorithm coverage.

#### Pipeline Architecture
**Workflow System** (`operations/workflow_pipeline.py`):
- Pipeline definition using step-based composition
- JSON serialization for pipeline persistence
- Reusable pipeline templates for common cleaning scenarios
- Execution history and logging

**Batch Processing** (`operations/batch_processor.py`):
- Template-based cleaning for multiple files
- Cleaning step serialization and reuse
- Predefined templates for common data cleaning tasks

**Design Decision**: Pipeline architecture enables automation and repeatability. JSON-based storage allows easy sharing and version control of cleaning workflows.

### Data Storage Solutions

#### File Format Support
**Data Loader** (`utils/data_loader.py`):
- Supported formats: CSV, Excel (xlsx/xls), JSON, Parquet, TSV, TXT
- Automatic encoding detection using `chardet` library
- Automatic separator detection for delimited files
- Configurable parsing parameters

**Quality Assessment** (`utils/quality_assessment.py`):
- Weighted scoring system: Completeness (40%), Consistency (30%), Uniqueness (20%), Validity (10%)
- Column-level and dataset-level quality metrics
- Automated recommendation generation

#### Database Integration
**Database Connector** (`utils/database_connector.py`):
- **Supported databases**: PostgreSQL, MySQL
- **SQLAlchemy-based** connection management for database abstraction
- **Import capabilities**: Table browsing, schema inspection, custom SQL queries, row limiting
- **Export capabilities**: Replace/Append/Fail modes, automatic table creation
- Secure credential handling through connection parameters

**Design Decision**: SQLAlchemy provides database-agnostic interface, allowing future expansion to other SQL databases. Connection pooling and parameterized queries ensure security and performance.

### Visualization Layer

#### Chart Generation
**Chart Generator** (`visualization/charts.py`):
- **Plotly-based** interactive visualizations
- Chart types: histograms, box plots, scatter plots, line charts, heatmaps
- Configurable binning, grouping, and styling options

**Dashboard System**:
- **Basic Dashboard** (`visualization/dashboard.py`): Predefined layouts (2x2, single row, single column) with subplot composition
- **Advanced Dashboard Builder** (`visualization/dashboard_builder_advanced.py`): 
  - Widget-based architecture with unique IDs
  - Position and size configuration for custom layouts
  - JSON serialization for dashboard persistence and sharing
  - Export to standalone HTML

**Design Decision**: Plotly provides interactive, publication-quality visualizations with built-in interactivity. Widget-based dashboard architecture allows flexible composition and reusability.

### Authentication and Authorization
**Current State**: No authentication system implemented. The application operates in single-user session mode.

**Future Consideration**: Multi-user deployment would require session isolation, user authentication, and role-based access control for shared pipelines and templates.

## External Dependencies

### Core Libraries
- **pandas**: Primary data manipulation and analysis
- **numpy**: Numerical computing and array operations
- **streamlit**: Web application framework and UI components

### Machine Learning
- **scikit-learn**: ML algorithms for:
  - Isolation Forest (anomaly detection)
  - KNN Imputer (missing value imputation)
  - DBSCAN (cluster-based outlier detection)
  - PCA (dimensionality reduction)
  - StandardScaler, LabelEncoder, OrdinalEncoder (preprocessing)

### Database Connectivity
- **SQLAlchemy**: Database abstraction and ORM
- **pymysql**: MySQL database driver (implied by connection string format)
- **psycopg2** (implied): PostgreSQL database driver

### Visualization
- **plotly**: Interactive chart generation
  - `plotly.express`: High-level plotting interface
  - `plotly.graph_objects`: Low-level figure construction
  - `plotly.subplots`: Multi-chart dashboard composition

### Utilities
- **chardet**: Automatic character encoding detection for file uploads
- **pathlib**: File path operations
- **json**: Template and pipeline serialization
- **uuid**: Unique identifier generation for widgets and pipelines
- **datetime**: Timestamp generation for operations and history

### File Format Support
- **openpyxl** (implied): Excel file reading/writing
- **pyarrow** (implied): Parquet file support