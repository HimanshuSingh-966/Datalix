# 🚀 Datalix - Advanced Data Cleaning Platform

<div align="center">

![Platform](https://img.shields.io/badge/Platform-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)

### 🌐 [**Try Live Demo →**](https://datalix.onrender.com/)

</div>

## Enterprise-Grade Data Cleaning with ML Intelligence

> A comprehensive, ML-powered data cleaning and preprocessing platform built with Streamlit. Transform messy datasets into analysis-ready data with advanced ML algorithms, database connectivity, batch processing, and automated workflows. Perfect for data scientists, analysts, and engineers who demand professional-grade data quality.

**🎯 [Launch Application](https://datalix.onrender.com/) | [View Documentation](#-quick-start) | [Report Issues](https://github.com/HimanshuSingh-966/datalix/issues)**

## 🌟 Key Features

### 🧠 ML-Powered Intelligence
- **Multivariate Anomaly Detection**: Isolation Forest algorithm for detecting complex outliers across multiple dimensions
- **Smart Cleaning Suggestions**: AI-driven recommendations with priority scoring (High/Medium/Low)
- **Pattern Recognition**: Automatic detection of emails, phones, URLs, dates, and formatting issues
- **Cluster-Based Analysis**: DBSCAN clustering for sophisticated outlier identification
- **Dimensionality Reduction**: PCA analysis with explained variance tracking
- **ML Imputation**: K-Nearest Neighbors algorithm for intelligent missing value prediction

### 🗄️ Database Connectivity
- **PostgreSQL Support**: Full integration with PostgreSQL databases
- **MySQL Support**: Native MySQL connectivity and operations
- **Direct Import**: Browse tables, inspect schemas, execute custom SQL queries
- **Smart Export**: Replace, append, or fail-safe modes with automatic table creation
- **Connection Management**: Secure credential handling and connection pooling via SQLAlchemy
- **Query Builder**: Custom SQL support with row limiting for large datasets

### 📦 Batch Processing System
- **Multi-File Processing**: Handle multiple datasets simultaneously with progress tracking
- **Cleaning Templates**: Reusable workflow templates for standardized cleaning operations
- **Predefined Templates**: Industry-standard templates (Basic, Standard, Text, Numeric cleaning)
- **Custom Templates**: Create, save, and share your own cleaning workflows
- **Batch Export**: Export all processed files in your preferred format
- **Operation Logging**: Detailed logs for every cleaning step applied

### 🔄 Workflow Pipelines
- **Visual Pipeline Builder**: Create multi-step data transformation workflows
- **Pipeline Management**: Save, load, and share pipeline configurations (JSON format)
- **Step-by-Step Execution**: Granular control with detailed logging per step
- **Execution History**: Track last 10 runs with performance metrics
- **Error Tracking**: Comprehensive error handling with detailed feedback
- **Predefined Pipelines**: Ready-to-use workflows (Basic Cleaning, ML Preparation, Advanced Cleaning)
- **Flexible Operations**: Chain cleaning, encoding, imputation, and ML operations

### 📊 Advanced Dashboard Builder
- **Widget System**: 8 widget types (histogram, scatter, line, bar, box, heatmap, metric, table)
- **Custom Layouts**: Configurable grid layouts (rows × columns)
- **Interactive Charts**: Plotly-powered visualizations with hover, zoom, and pan
- **Dashboard Management**: Create, save, load, and export multiple dashboards
- **HTML Export**: Share dashboards as standalone, interactive HTML files
- **Live Preview**: Real-time dashboard rendering with your data
- **Theme Support**: Professional dark theme for reduced eye strain

### 📁 Universal Data Support
- **File Formats**: CSV, Excel (.xlsx, .xls), JSON, Parquet, TSV, TXT
- **Encoding Detection**: Automatic character encoding detection with chardet
- **Separator Detection**: Smart delimiter detection for text files
- **Large File Handling**: Efficient processing of large datasets
- **Data Preview**: Instant preview with statistics and quality assessment

### 🧹 Comprehensive Data Cleaning
- **Auto-Clean Workflow**: One-click automated cleaning with intelligent defaults
- **Missing Value Handling**: Mean, median, mode, KNN imputation, forward/backward fill, interpolation
- **Outlier Detection**: IQR, Z-Score, and Isolation Forest methods
- **Duplicate Removal**: Identify and remove exact and near-duplicate records
- **Text Normalization**: Lowercase, uppercase, whitespace trimming, special character removal
- **Data Type Conversion**: Smart type inference and conversion
- **Column Operations**: Drop, rename, and transform columns
- **Categorical Encoding**: Label encoding, one-hot encoding, ordinal encoding

### 📈 Data Quality Assessment
- **Quality Scoring**: Weighted scoring system (0-100 scale)
  - Completeness (40%): Missing value analysis
  - Consistency (30%): Format and pattern validation
  - Uniqueness (20%): Duplicate detection
  - Validity (10%): Outlier and anomaly identification
- **Column-Level Metrics**: Individual quality scores per column
- **Automated Recommendations**: Actionable suggestions for improvement
- **Before/After Comparison**: Track quality improvements over time

### 🎨 Rich Visualizations
- **Basic Charts**: Histogram, box plot, scatter plot, line chart, bar chart, pie chart
- **Statistical Plots**: Correlation heatmap, distribution analysis, pair plots
- **Interactive Features**: Hover tooltips, zooming, panning, selection
- **Export Options**: Save charts as PNG, SVG, or interactive HTML
- **Dashboard Composition**: Multi-panel dashboards with custom layouts

### ⏮️ History & Undo System
- **Operation Tracking**: Complete history of all data operations
- **Undo/Redo**: Revert any operation (up to 50 steps)
- **State Snapshots**: Automatic snapshots before each operation
- **History Export**: Export operation logs for audit trails

## 🚀 Quick Start

### Online Access

**🌐 Visit [datalix-new.streamlit.app](https://datalix.onrender.com/)** to start using Datalix immediately—no installation required!

### Local Installation

1. **Clone the repository**:
```bash
git clone https://github.com/HimanshuSingh-966/datalix.git
cd datalix
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure Streamlit** (already set up in `.streamlit/config.toml`):
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "dark"
```

4. **Run the application**:
```bash
streamlit run app.py --server.port 5000
```

5. **Open your browser** and navigate to `http://localhost:5000`

### First Steps

1. **📤 Data Upload**: Upload your dataset (CSV, Excel, JSON, Parquet) or connect to a database
2. **🔍 Data Preview**: Explore your data with statistics and visualizations
3. **📊 Quality Assessment**: Review automated quality scoring and recommendations
4. **🧹 Data Cleaning**: Apply cleaning operations or use auto-clean workflow
5. **🤖 ML Cleaning**: Leverage ML for anomaly detection and smart suggestions
6. **🔄 Workflows**: Create reusable pipelines for repeated operations
7. **📦 Batch Processing**: Process multiple files with standardized templates
8. **📊 Dashboard Builder**: Create custom dashboards for data exploration
9. **💾 Export**: Download cleaned data or export to database

## 📚 How It Works

### Data Quality Scoring Algorithm
The platform employs a sophisticated weighted scoring system:

```python
Quality Score = (Completeness × 0.40) + (Consistency × 0.30) + 
                (Uniqueness × 0.20) + (Validity × 0.10)
```

- **Completeness**: Percentage of non-missing values
- **Consistency**: Format uniformity and pattern adherence
- **Uniqueness**: Ratio of unique records to total records
- **Validity**: Outlier-free percentage using statistical methods

### ML Anomaly Detection Pipeline

**Multivariate Anomaly Detection**:
```python
# Uses Isolation Forest algorithm
1. Select numerical columns
2. Apply StandardScaler normalization
3. Train Isolation Forest with configurable contamination
4. Score and label anomalies (-1 = outlier, 1 = normal)
5. One-click removal with data preservation
```

**Pattern Analysis**:
```python
# Text pattern recognition
1. Detect common patterns (email, phone, URL, date)
2. Calculate pattern consistency scores
3. Identify whitespace and formatting issues
4. Flag non-ASCII characters
5. Generate actionable recommendations
```

### Workflow Pipeline Architecture

**Pipeline Execution Flow**:
```python
Pipeline → Steps (ordered) → Operations → Logging → Results
         ↓
    JSON Serialization → Save/Load → Share
```

**Supported Operations**:
- Data Cleaning (duplicates, columns, missing values)
- Encoding (label, one-hot, ordinal)
- Outlier Management (IQR, Z-Score, Isolation Forest)
- ML Operations (anomaly detection, imputation)
- Transformations (log, sqrt, square)
- Filtering (pandas query syntax)

### Batch Processing Workflow

**Template-Based Processing**:
```python
Template Definition → Multi-File Upload → Apply Template → 
    Progress Tracking → Batch Export
```

**Template Structure**:
```python
{
    "name": "Standard Cleaning",
    "operations": [
        {"type": "remove_duplicates"},
        {"type": "drop_high_missing_columns", "threshold": 0.5},
        {"type": "impute_missing", "method": "median"},
        {"type": "remove_outliers", "method": "iqr"}
    ]
}
```

## 🎯 Use Cases

### For Data Scientists
- **ML Preprocessing**: Prepare datasets for machine learning pipelines
- **Feature Engineering**: Transform and encode features systematically
- **Outlier Analysis**: Identify and handle anomalous data points
- **Pipeline Automation**: Create reusable workflows for standard preprocessing
- **Quality Assurance**: Validate data quality before model training

### For Data Engineers
- **ETL Operations**: Extract, transform, and load data with automated workflows
- **Database Integration**: Import from and export to PostgreSQL/MySQL databases
- **Batch Processing**: Handle multiple files with standardized cleaning rules
- **Data Validation**: Ensure data quality meets enterprise standards
- **Audit Trails**: Track all data operations with comprehensive logging

### For Business Analysts
- **Self-Service Cleaning**: Clean data without coding or technical expertise
- **Dashboard Creation**: Build interactive dashboards for stakeholder presentations
- **Quality Reporting**: Generate data quality reports with scores and recommendations
- **Template Management**: Standardize cleaning processes across teams
- **Visual Analysis**: Explore data with interactive charts and visualizations

### For Non-Technical Users
- **Intuitive Interface**: Excel-like experience with guided workflows
- **AI Assistance**: Get automated suggestions and recommendations
- **Visual Feedback**: See immediate results with before/after comparisons
- **Error Prevention**: Built-in validation prevents common mistakes
- **Learning Resources**: Comprehensive help section with examples

## 🔧 Technical Architecture

### Core Technologies
- **Framework**: Streamlit 1.30+ (Python web framework)
- **Data Processing**: Pandas 2.0+, NumPy 1.24+
- **Machine Learning**: Scikit-learn 1.3+ (Isolation Forest, KNN, DBSCAN, PCA)
- **Visualization**: Plotly 5.18+ (interactive charts)
- **Database**: SQLAlchemy 2.0+, psycopg2-binary, PyMySQL
- **Utilities**: chardet (encoding detection), openpyxl (Excel support)

### Project Structure

```
datalix/
├── app.py                              # Main application entry point
├── core/
│   ├── session_manager.py             # Centralized session state management
│   └── history_tracker.py             # Undo/redo functionality (50 steps)
├── operations/
│   ├── cleaning.py                    # Basic cleaning operations
│   ├── encoding.py                    # Categorical encoding methods
│   ├── imputation.py                  # Missing value imputation
│   ├── ml_cleaning.py                 # ML-based cleaning (NEW)
│   ├── batch_processor.py             # Batch file processing (NEW)
│   └── workflow_pipeline.py           # Pipeline management (NEW)
├── utils/
│   ├── data_loader.py                 # Multi-format data loading
│   ├── quality_assessment.py          # Quality scoring engine
│   ├── encoding_detector.py           # Encoding detection
│   └── database_connector.py          # Database connectivity (NEW)
├── visualization/
│   ├── charts.py                      # Chart generation
│   ├── dashboard.py                   # Basic dashboard layouts
│   └── dashboard_builder_advanced.py  # Advanced dashboard builder (NEW)
└── .streamlit/
    └── config.toml                    # Dark theme configuration
```

### Key Algorithms

#### Isolation Forest Anomaly Detection
```python
from sklearn.ensemble import IsolationForest

# Multivariate outlier detection
iso_forest = IsolationForest(
    contamination=0.1,      # Expected outlier percentage
    random_state=42,
    n_estimators=100
)
anomaly_labels = iso_forest.fit_predict(scaled_data)
anomaly_scores = iso_forest.score_samples(scaled_data)
```

#### KNN Imputation
```python
from sklearn.impute import KNNImputer

# Intelligent missing value imputation
knn_imputer = KNNImputer(
    n_neighbors=5,
    weights='distance'
)
imputed_data = knn_imputer.fit_transform(data)
```

#### DBSCAN Clustering
```python
from sklearn.cluster import DBSCAN

# Density-based outlier detection
dbscan = DBSCAN(
    eps=0.5,                # Neighborhood radius
    min_samples=5           # Minimum cluster size
)
cluster_labels = dbscan.fit_predict(scaled_data)
outliers = data[cluster_labels == -1]  # Noise points
```

## 🎨 Dashboard Widget Gallery

### Available Widgets

1. **Histogram**: Distribution analysis with configurable bins
2. **Box Plot**: Statistical summary with outlier visualization
3. **Scatter Plot**: Correlation analysis with optional color coding
4. **Line Chart**: Time series and trend visualization
5. **Bar Chart**: Categorical comparison and aggregation
6. **Heatmap**: Correlation matrices and pattern detection
7. **Metric**: Single KPI display (mean, sum, count, max, min)
8. **Table**: Tabular data view with column filtering

### Dashboard Export Options

- **JSON Configuration**: Save dashboard layout and widget settings
- **Interactive HTML**: Standalone file with full interactivity
- **Share & Collaborate**: Exchange dashboard configs with team members

## 🔧 Advanced Features

### Database Operations

**PostgreSQL Connection**:
```python
# Connection parameters
host = "localhost"
port = 5432
database = "mydb"
user = "postgres"
password = "secure_password"

# Import data
SELECT * FROM customers WHERE signup_date > '2024-01-01' LIMIT 10000

# Export data
df.to_sql('cleaned_customers', con=engine, if_exists='replace')
```

**MySQL Connection**:
```python
# Connection string format
mysql+pymysql://user:password@host:port/database

# Features: table browsing, schema inspection, custom queries
```

### Batch Processing Templates

**Create Custom Template**:
```python
template = CleaningTemplate(
    name="Custom Sales Cleaning",
    operations=[
        {"type": "remove_duplicates"},
        {"type": "drop_columns", "columns": ["temp_id"]},
        {"type": "impute", "column": "revenue", "method": "median"},
        {"type": "encode", "column": "category", "method": "onehot"},
        {"type": "remove_outliers", "columns": ["revenue"], "method": "iqr"}
    ]
)
template.save("templates/sales_cleaning.json")
```

**Apply to Multiple Files**:
```python
processor = BatchProcessor()
results = processor.process_batch(
    files=uploaded_files,
    template=template,
    export_format="csv"
)
```

### Workflow Pipeline Examples

**ML Preparation Pipeline**:
```python
pipeline = Pipeline(name="ML Prep Pipeline")
pipeline.add_step("Remove Duplicates", "remove_duplicates", {})
pipeline.add_step("Drop High Missing", "drop_columns_threshold", {"threshold": 0.3})
pipeline.add_step("KNN Imputation", "knn_impute", {"n_neighbors": 5})
pipeline.add_step("Detect Anomalies", "ml_anomaly_detection", {"contamination": 0.05})
pipeline.add_step("Remove Anomalies", "remove_anomalies", {})
pipeline.add_step("Label Encode", "label_encode", {"columns": ["category"]})

# Execute and log
results = pipeline.execute(df)
pipeline.save("pipelines/ml_prep.json")
```

## 🚀 Performance Features

### Large Dataset Handling
- **Chunked Processing**: Process files larger than memory in chunks
- **Memory Optimization**: Efficient data type inference and usage
- **Lazy Loading**: Load data only when needed
- **Progress Tracking**: Real-time progress bars for long operations

### Scalability
- **Session Isolation**: Each user session is independent
- **State Management**: Efficient session state with minimal overhead
- **Caching**: Streamlit caching for expensive computations
- **Database Connection Pooling**: Reuse connections for efficiency

## 🔒 Security & Privacy

### Data Protection
- **Local Processing**: All data processing occurs on the server, not sent to third parties
- **Session Isolation**: User data is isolated per session
- **Secure Database Connections**: Encrypted connections via SQLAlchemy
- **No Data Persistence**: Data cleared when session ends (unless explicitly saved)

### Security Best Practices
- **SQL Injection Prevention**: Parameterized queries and SQLAlchemy ORM
- **Credential Security**: No hardcoded credentials, environment variable support
- **Input Validation**: Comprehensive validation of user inputs
- **Error Handling**: Safe error messages without exposing sensitive information

## 🤝 Contributing

We welcome contributions to Datalix! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with clear, commented code
4. **Test thoroughly** with various datasets
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request** with detailed description

### Development Setup

```bash
# Clone repository
git clone https://github.com/HimanshuSingh-966/datalix.git
cd datalix

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py --server.port 5000

# Run in development mode with auto-reload
streamlit run app.py --server.port 5000 --server.runOnSave true
```

### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include type hints for function parameters and returns
- Write unit tests for new features
- Update documentation for user-facing changes

## 📈 Roadmap

### Current Version: 2.0.0 (Enhanced Edition)
✅ Database connectivity (PostgreSQL, MySQL)  
✅ ML-based data cleaning with Isolation Forest  
✅ Batch processing with template system  
✅ Workflow pipeline builder  
✅ Advanced dashboard builder  
✅ Dark theme UI  

### Version 2.1.0 (Planned)
- 🔄 Scheduled pipeline execution
- 🔄 Data versioning and rollback
- 🔄 Export to additional databases (MongoDB, SQLite)
- 🔄 Enhanced pattern detection (credit cards, SSNs)
- 🔄 API endpoint for programmatic access

### Version 2.2.0 (Future)
- 🔮 Real-time data streaming support
- 🔮 Cloud storage integration (S3, GCS, Azure)
- 🔮 Advanced statistical tests (hypothesis testing)
- 🔮 Time series forecasting
- 🔮 Natural language query interface

### Version 3.0.0 (Long-term Vision)
- 🌟 Multi-user collaboration features
- 🌟 Role-based access control
- 🌟 Enterprise SSO integration
- 🌟 Data lineage tracking
- 🌟 Automated report generation
- 🌟 Integration with BI tools (Tableau, Power BI)

## 📞 Support & Community

### Documentation
- **User Guide**: Comprehensive step-by-step instructions (see Help section in app)
- **API Reference**: Technical documentation for developers
- **Video Tutorials**: Coming soon
- **Sample Projects**: Example workflows and templates included

### Getting Help
- **Live Demo**: [datalix-new.streamlit.app](https://datalix.onrender.com/)
- **GitHub Issues**: [Report bugs and request features](https://github.com/HimanshuSingh-966/datalix/issues)
- **Discussions**: [Ask questions and share ideas](https://github.com/HimanshuSingh-966/datalix/discussions)
- **Email Support**: himanshu.singh.2kfive@gmail.com

### Community Resources
- Share your templates and pipelines
- Contribute sample datasets
- Write tutorials and guides
- Translate documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team**: For the incredible web framework that makes Python web apps effortless
- **Pandas Contributors**: For the most powerful data manipulation library
- **Plotly Team**: For beautiful, interactive visualizations
- **Scikit-learn Community**: For comprehensive machine learning algorithms
- **SQLAlchemy Developers**: For the best Python database toolkit
- **Open Source Community**: For the thousands of libraries that make this possible

## 📊 Project Statistics

- **Lines of Code**: ~5,000+
- **Modules**: 13 Python files
- **Features**: 30+ data cleaning operations
- **ML Algorithms**: 5 (Isolation Forest, KNN, DBSCAN, PCA, StandardScaler)
- **Visualization Types**: 15+ chart types
- **Database Support**: 2 (PostgreSQL, MySQL)
- **File Formats**: 6 (CSV, Excel, JSON, Parquet, TSV, TXT)
- **Development Time**: Enhanced from original platform
- **Version**: 2.0.0 - Enhanced Edition

---

**Made with ❤️ for the data community**

*Transform your messy data into clean, analysis-ready datasets with enterprise-grade ML intelligence.*

## 🔗 Quick Links

- [🌐 Live Demo](https://datalix.onrender.com/)
- [🚀 Quick Start](#quick-start)
- [📚 How It Works](#how-it-works)
- [🎯 Use Cases](#use-cases)
- [🔧 Technical Architecture](#technical-architecture)
- [🎨 Dashboard Widget Gallery](#dashboard-widget-gallery)
- [🔧 Advanced Features](#advanced-features)
- [🤝 Contributing](#contributing)
- [📈 Roadmap](#roadmap)
- [📞 Support & Community](#support--community)

---

<div align="center">

**Datalix v2.0.0** | **Enterprise-Grade Data Cleaning** | **Built with Streamlit**

[🌐 Live Demo](https://datalix.onrender.com/) | [⭐ Star on GitHub](https://github.com/HimanshuSingh-966/datalix) | [🐛 Report Bug](https://github.com/HimanshuSingh-966/datalix/issues) | [💡 Request Feature](https://github.com/HimanshuSingh-966/datalix/issues)

</div>
