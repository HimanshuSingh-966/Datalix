"""
Datalix - Advanced Data Cleaning and Preprocessing Platform
Enhanced version with optimized performance and modern UI/UX
"""

import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import io

# Import utility modules
from utils.data_loader import DataLoader
from utils.quality_assessment import QualityAssessor
from utils.encoding_detector import EncodingDetector

# Import operation modules
from operations.cleaning import DataCleaner
from operations.encoding import CategoricalEncoder
from operations.imputation import MissingValueImputer

# Import visualization modules
from visualization.charts import ChartGenerator
from visualization.dashboard import DashboardBuilder

# Import core modules
from core.session_manager import SessionManager
from core.history_tracker import HistoryTracker

# Page configuration
st.set_page_config(
    page_title="Datalix - Data Cleaning Platform",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session manager
session_mgr = SessionManager()

# Auto-scroll to top function
def scroll_to_top():
    """Scroll to top of page using JavaScript"""
    import streamlit.components.v1 as components
    components.html(
        """
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
        """,
        height=0,
    )

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'original_data' not in st.session_state:
    st.session_state.original_data = None
if 'file_info' not in st.session_state:
    st.session_state.file_info = {}
if 'history' not in st.session_state:
    st.session_state.history = HistoryTracker()
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'quality_score' not in st.session_state:
    st.session_state.quality_score = None

# Sidebar navigation
with st.sidebar:
    st.title("🔧 Datalix")
    st.markdown("---")
    
    # Navigation menu
    pages = {
        "Home": "🏠",
        "Data Upload": "📁",
        "Data Preview": "👁️",
        "Data Profiling": "📊",
        "Data Cleaning": "🧹",
        "Missing Values": "❓",
        "Outlier Detection": "🎯",
        "Encoding": "🔤",
        "Visualization": "📈",
        "Export": "💾",
        "Help": "❓"
    }
    
    selected_page = st.radio(
        "Navigation",
        list(pages.keys()),
        format_func=lambda x: f"{pages[x]} {x}",
        key="nav_radio"
    )
    
    # Auto-scroll when page changes
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        scroll_to_top()
    
    st.markdown("---")
    
    # Data info sidebar
    if st.session_state.data is not None:
        st.subheader("📋 Data Info")
        df = st.session_state.data
        st.metric("Rows", f"{len(df):,}")
        st.metric("Columns", len(df.columns))
        
        if st.session_state.quality_score is not None:
            score = st.session_state.quality_score['overall_score']
            st.metric("Quality Score", f"{score:.1f}/100")
        
        # History info
        history_count = len(st.session_state.history.history)
        if history_count > 0:
            st.metric("Operations", history_count)
    
    st.markdown("---")
    st.caption("Version 2.0.0 | Enhanced Edition")

# Main content area
if selected_page == "Home":
    scroll_to_top()
    st.title("🏠 Welcome to Datalix")
    st.markdown("### Your Advanced Data Cleaning and Preprocessing Platform")
    
    st.markdown("""
    Datalix is a powerful, no-code platform for cleaning, preprocessing, and analyzing your data.
    With advanced features like ML-based imputation, automatic encoding detection, and interactive
    visualizations, you can transform messy data into clean, analysis-ready datasets.
    """)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🚀 Fast & Efficient")
        st.markdown("""
        - Handles files up to 200MB
        - Chunked processing
        - Instant preview (1000 rows)
        - Lazy loading & pagination
        """)
    
    with col2:
        st.markdown("### 🎯 Smart Features")
        st.markdown("""
        - Auto encoding detection
        - ML-based imputation
        - Smart data profiling
        - One-click cleaning
        """)
    
    with col3:
        st.markdown("### 📊 Rich Visualizations")
        st.markdown("""
        - Interactive charts
        - Correlation heatmaps
        - Distribution analysis
        - Custom dashboards
        """)
    
    st.markdown("---")
    
    # Quick start guide
    st.subheader("🎯 Quick Start Guide")
    
    steps = st.tabs(["1️⃣ Upload", "2️⃣ Profile", "3️⃣ Clean", "4️⃣ Export"])
    
    with steps[0]:
        st.markdown("""
        **Upload Your Data**
        
        1. Go to the 'Data Upload' page
        2. Choose your file (CSV, Excel, JSON, Parquet)
        3. Select encoding (or use auto-detection)
        4. Click 'Load Data'
        
        *Tip: You can upload files up to 200MB!*
        """)
    
    with steps[1]:
        st.markdown("""
        **Profile Your Data**
        
        1. Navigate to 'Data Profiling'
        2. Review data quality score
        3. Check missing values
        4. Identify data types
        
        *Tip: Quality score shows areas for improvement!*
        """)
    
    with steps[2]:
        st.markdown("""
        **Clean Your Data**
        
        1. Use 'Data Cleaning' for duplicates
        2. Go to 'Missing Values' for imputation
        3. Check 'Outlier Detection' for anomalies
        4. Use 'Encoding' for categorical data
        
        *Tip: All operations are tracked and can be undone!*
        """)
    
    with steps[3]:
        st.markdown("""
        **Export Results**
        
        1. Go to 'Export' page
        2. Choose format (CSV, Excel, JSON)
        3. Select encoding
        4. Download your clean data
        
        *Tip: You can export at any stage!*
        """)
    
    if st.session_state.data is None:
        st.info("👈 Start by uploading your data from the sidebar!")

elif selected_page == "Data Upload":
    scroll_to_top()
    st.title("📁 Data Upload")
    st.markdown("Upload your data file or use sample datasets to get started.")
    
    # Create tabs for different upload methods
    upload_tabs = st.tabs(["📎 File Upload", "🔗 URL Import", "📋 Sample Data"])
    
    with upload_tabs[0]:
        st.subheader("Upload Data File")
        
        # File uploader with multiple format support
        uploaded_files = st.file_uploader(
            "Choose file(s) to upload",
            type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'tsv', 'txt'],
            accept_multiple_files=True,
            help="Supports CSV, Excel, JSON, Parquet, TSV, TXT files up to 200MB"
        )
        
        # Encoding selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            encoding_options = ['Auto-detect', 'UTF-8', 'Latin-1', 'ISO-8859-1', 'Windows-1252', 'ASCII']
            selected_encoding = st.selectbox(
                "File Encoding",
                encoding_options,
                help="Select 'Auto-detect' to automatically detect file encoding"
            )
        
        with col2:
            st.markdown("###")  # Spacing
            load_button = st.button("🚀 Load Data", type="primary", use_container_width=True)
        
        if uploaded_files and load_button:
            with st.spinner("Loading data..."):
                try:
                    loader = DataLoader()
                    
                    # Detect encoding if auto-detect is selected
                    if selected_encoding == 'Auto-detect':
                        detector = EncodingDetector()
                        detected_encoding = detector.detect_encoding(uploaded_files[0])
                        st.info(f"✓ Detected encoding: {detected_encoding}")
                        encoding = detected_encoding
                    else:
                        encoding = selected_encoding
                    
                    # Load data with progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("Reading file...")
                    progress_bar.progress(30)
                    
                    df = loader.load_file(uploaded_files[0], encoding=encoding)
                    
                    status_text.text("Processing data...")
                    progress_bar.progress(60)
                    
                    # Store in session state
                    st.session_state.data = df
                    st.session_state.original_data = df.copy()
                    st.session_state.file_info = {
                        'filename': uploaded_files[0].name,
                        'encoding': encoding,
                        'size': uploaded_files[0].size,
                        'rows': len(df),
                        'columns': len(df.columns)
                    }
                    
                    # Calculate quality score
                    assessor = QualityAssessor()
                    st.session_state.quality_score = assessor.calculate_quality_score(df)
                    
                    status_text.text("Complete!")
                    progress_bar.progress(100)
                    
                    st.success(f"✓ Successfully loaded {len(df):,} rows and {len(df.columns)} columns!")
                    
                    # Clear progress indicators
                    status_text.empty()
                    progress_bar.empty()
                    
                except Exception as e:
                    st.error(f"❌ Error loading file: {str(e)}")
    
    with upload_tabs[1]:
        st.subheader("Import from URL")
        
        url = st.text_input(
            "Enter data URL",
            placeholder="https://example.com/data.csv",
            help="Provide a direct link to CSV or JSON file"
        )
        
        if st.button("📥 Import from URL", type="primary"):
            if url:
                with st.spinner("Importing data..."):
                    try:
                        loader = DataLoader()
                        df = loader.load_from_url(url)
                        
                        st.session_state.data = df
                        st.session_state.original_data = df.copy()
                        st.session_state.file_info = {
                            'filename': url.split('/')[-1],
                            'encoding': 'UTF-8',
                            'source': 'url',
                            'rows': len(df),
                            'columns': len(df.columns)
                        }
                        
                        # Calculate quality score
                        assessor = QualityAssessor()
                        st.session_state.quality_score = assessor.calculate_quality_score(df)
                        
                        st.success(f"✓ Successfully imported {len(df):,} rows!")
                        
                    except Exception as e:
                        st.error(f"❌ Error importing from URL: {str(e)}")
            else:
                st.warning("Please enter a valid URL")
    
    with upload_tabs[2]:
        st.subheader("Sample Datasets")
        st.markdown("Try Datalix with our sample datasets")
        
        sample_options = {
            "Sales Data": "1000 rows of sales transactions",
            "Customer Data": "500 customer records",
            "Financial Data": "252 days of stock data"
        }
        
        selected_sample = st.selectbox(
            "Choose a sample dataset",
            list(sample_options.keys()),
            format_func=lambda x: f"{x} - {sample_options[x]}"
        )
        
        if st.button("📊 Load Sample Data", type="primary"):
            with st.spinner("Loading sample data..."):
                loader = DataLoader()
                df = loader.load_sample_data(selected_sample)
                
                st.session_state.data = df
                st.session_state.original_data = df.copy()
                st.session_state.file_info = {
                    'filename': f"{selected_sample}.csv",
                    'encoding': 'UTF-8',
                    'source': 'sample',
                    'rows': len(df),
                    'columns': len(df.columns)
                }
                
                # Calculate quality score
                assessor = QualityAssessor()
                st.session_state.quality_score = assessor.calculate_quality_score(df)
                
                st.success(f"✓ Loaded {selected_sample} with {len(df):,} rows!")

elif selected_page == "Data Preview":
    scroll_to_top()
    st.title("👁️ Data Preview")
    
    if st.session_state.data is None:
        st.warning("No data loaded. Please upload a file first.")
    else:
        df = st.session_state.data
        
        # Preview controls
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            rows_to_show = st.slider(
                "Rows to display",
                min_value=10,
                max_value=min(1000, len(df)),
                value=min(100, len(df)),
                step=10
            )
        
        with col2:
            page_size = st.selectbox("Page size", [25, 50, 100, 200], index=1)
        
        with col3:
            st.markdown("###")  # Spacing
            show_stats = st.checkbox("Show stats", value=True)
        
        # File information
        if st.session_state.file_info:
            info = st.session_state.file_info
            st.info(f"📄 **{info.get('filename', 'Unknown')}** | "
                   f"Encoding: {info.get('encoding', 'Unknown')} | "
                   f"Size: {info.get('size', 0) / 1024:.1f} KB")
        
        # Pagination
        total_pages = (rows_to_show - 1) // page_size + 1
        page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
        
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, rows_to_show)
        
        # Display data
        st.dataframe(
            df.iloc[start_idx:end_idx],
            use_container_width=True,
            height=400
        )
        
        st.caption(f"Showing rows {start_idx + 1} to {end_idx} of {rows_to_show} (Total: {len(df):,} rows)")
        
        if show_stats:
            st.markdown("---")
            st.subheader("📊 Quick Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Rows", f"{len(df):,}")
            
            with col2:
                st.metric("Total Columns", len(df.columns))
            
            with col3:
                missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
                st.metric("Missing Values", f"{missing_pct:.1f}%")
            
            with col4:
                duplicates = df.duplicated().sum()
                st.metric("Duplicates", f"{duplicates:,}")

elif selected_page == "Data Profiling":
    scroll_to_top()
    st.title("📊 Data Profiling Dashboard")
    
    if st.session_state.data is None:
        st.warning("No data loaded. Please upload a file first.")
    else:
        df = st.session_state.data
        assessor = QualityAssessor()
        
        # Calculate or use cached quality score
        if st.session_state.quality_score is None:
            st.session_state.quality_score = assessor.calculate_quality_score(df)
        
        quality_data = st.session_state.quality_score
        
        # Overall quality score
        st.subheader("🎯 Overall Data Quality Score")
        
        score = quality_data['overall_score']
        color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.metric(
                label="Quality Score",
                value=f"{score:.1f}/100",
                delta=None
            )
            st.progress(score / 100)
            st.markdown(f"{color} {quality_data['grade']}")
        
        st.markdown("---")
        
        # Quality metrics breakdown
        st.subheader("📈 Quality Metrics Breakdown")
        
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            st.metric(
                "Completeness",
                f"{quality_data['completeness_score']:.1f}%",
                help="Percentage of non-missing values"
            )
        
        with metrics_col2:
            st.metric(
                "Consistency",
                f"{quality_data['consistency_score']:.1f}%",
                help="Data formatting consistency"
            )
        
        with metrics_col3:
            st.metric(
                "Uniqueness",
                f"{quality_data['uniqueness_score']:.1f}%",
                help="Percentage of unique records"
            )
        
        with metrics_col4:
            st.metric(
                "Validity",
                f"{quality_data['validity_score']:.1f}%",
                help="Data within expected ranges"
            )
        
        st.markdown("---")
        
        # Data type analysis
        st.subheader("🔤 Data Type Distribution")
        
        type_counts = df.dtypes.value_counts()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Data type summary
            for dtype, count in type_counts.items():
                st.markdown(f"**{dtype}**: {count} columns")
        
        with col2:
            # Column details
            st.markdown("**Column Details:**")
            for col in df.columns[:10]:  # Show first 10
                st.text(f"{col}: {df[col].dtype}")
            
            if len(df.columns) > 10:
                st.caption(f"... and {len(df.columns) - 10} more columns")
        
        st.markdown("---")
        
        # Missing values analysis
        st.subheader("❓ Missing Values Analysis")
        
        missing_data = assessor.analyze_missing_values(df)
        
        if missing_data['total_missing'] > 0:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.metric("Total Missing Values", f"{missing_data['total_missing']:,}")
                st.metric("Affected Columns", missing_data['columns_with_missing'])
            
            with col2:
                st.metric("Missing Percentage", f"{missing_data['missing_percentage']:.2f}%")
                
                if missing_data['columns_with_missing'] > 0:
                    worst_col = missing_data['missing_by_column'].idxmax()
                    worst_pct = missing_data['missing_by_column'].max()
                    st.metric("Worst Column", worst_col)
                    st.caption(f"{worst_pct:.1f}% missing")
            
            # Show columns with missing values
            if missing_data['columns_with_missing'] > 0:
                st.markdown("**Columns with Missing Values:**")
                missing_cols_df = pd.DataFrame({
                    'Column': missing_data['missing_by_column'].index,
                    'Missing Count': missing_data['missing_by_column'].values,
                    'Percentage': (missing_data['missing_by_column'].values / len(df) * 100).round(2)
                })
                st.dataframe(missing_cols_df, use_container_width=True, height=200)
        else:
            st.success("✓ No missing values detected!")
        
        st.markdown("---")
        
        # Duplicates analysis
        st.subheader("🔄 Duplicate Records")
        
        duplicates = df.duplicated().sum()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.metric("Duplicate Rows", f"{duplicates:,}")
            if duplicates > 0:
                dup_pct = (duplicates / len(df)) * 100
                st.metric("Percentage", f"{dup_pct:.2f}%")
        
        with col2:
            if duplicates > 0:
                st.warning(f"⚠️ Found {duplicates:,} duplicate rows")
                if st.button("🗑️ Remove Duplicates"):
                    st.session_state.data = df.drop_duplicates()
                    st.session_state.history.add_operation("Remove Duplicates", df.copy())
                    st.success("✓ Duplicates removed!")
                    st.rerun()
            else:
                st.success("✓ No duplicates found!")
        
        st.markdown("---")
        
        # Recommendations
        st.subheader("💡 Improvement Suggestions")
        
        recommendations = quality_data.get('recommendations', [])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
        else:
            st.success("✓ Data quality is excellent! No immediate improvements needed.")

elif selected_page == "Data Cleaning":
    scroll_to_top()
    st.title("🧹 Data Cleaning Operations")
    
    if st.session_state.data is None:
        st.warning("No data loaded. Please upload a file first.")
    else:
        df = st.session_state.data
        cleaner = DataCleaner()
        
        # Cleaning operations tabs
        cleaning_tabs = st.tabs([
            "🚀 Auto-Clean",
            "🗑️ Remove Duplicates",
            "✂️ Remove Columns",
            "🔤 Text Cleaning",
            "🔄 Type Conversion"
        ])
        
        with cleaning_tabs[0]:
            st.subheader("Automated Cleaning Workflow")
            st.markdown("""
            Automatically clean your data with one click. This will:
            - Remove duplicate rows
            - Remove columns with >95% missing values
            - Convert data types appropriately
            - Standardize text formatting
            """)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if st.button("🚀 Start Auto-Clean", type="primary", use_container_width=True):
                    with st.spinner("Cleaning data..."):
                        try:
                            cleaned_df, operations = cleaner.auto_clean(df)
                            
                            st.session_state.history.add_operation("Auto-Clean", df.copy())
                            st.session_state.data = cleaned_df
                            
                            st.success("✓ Auto-clean completed!")
                            
                            st.markdown("**Operations performed:**")
                            for op in operations:
                                st.markdown(f"- {op}")
                            
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error during auto-clean: {str(e)}")
            
            with col2:
                if len(st.session_state.history.history) > 0:
                    if st.button("↩️ Undo Last", use_container_width=True):
                        previous_df = st.session_state.history.undo()
                        if previous_df is not None:
                            st.session_state.data = previous_df
                            st.success("✓ Undone!")
                            st.rerun()
        
        with cleaning_tabs[1]:
            st.subheader("Remove Duplicate Rows")
            
            duplicates = df.duplicated().sum()
            
            st.metric("Duplicate Rows Found", f"{duplicates:,}")
            
            if duplicates > 0:
                keep_option = st.radio(
                    "Keep which occurrence?",
                    ["first", "last"],
                    help="Which duplicate to keep"
                )
                
                subset_cols = st.multiselect(
                    "Consider only these columns (optional)",
                    df.columns.tolist(),
                    help="Leave empty to check all columns"
                )
                
                if st.button("🗑️ Remove Duplicates", type="primary"):
                    st.session_state.history.add_operation("Remove Duplicates", df.copy())
                    
                    if subset_cols:
                        st.session_state.data = df.drop_duplicates(subset=subset_cols, keep=keep_option)
                    else:
                        st.session_state.data = df.drop_duplicates(keep=keep_option)
                    
                    st.success(f"✓ Removed {duplicates:,} duplicate rows!")
                    st.rerun()
            else:
                st.info("No duplicates found!")
        
        with cleaning_tabs[2]:
            st.subheader("Remove Columns")
            
            st.markdown("**Remove columns based on criteria:**")
            
            # High missing values
            missing_threshold = st.slider(
                "Remove columns with missing values >",
                0, 100, 95,
                help="Columns with missing percentage above this will be removed"
            )
            
            cols_to_remove = []
            for col in df.columns:
                missing_pct = (df[col].isnull().sum() / len(df)) * 100
                if missing_pct > missing_threshold:
                    cols_to_remove.append(col)
            
            if cols_to_remove:
                st.warning(f"⚠️ {len(cols_to_remove)} columns will be removed:")
                st.write(cols_to_remove)
                
                if st.button("🗑️ Remove These Columns", type="primary"):
                    st.session_state.history.add_operation("Remove Columns", df.copy())
                    st.session_state.data = df.drop(columns=cols_to_remove)
                    st.success(f"✓ Removed {len(cols_to_remove)} columns!")
                    st.rerun()
            else:
                st.info(f"No columns with >{missing_threshold}% missing values")
            
            st.markdown("---")
            
            # Manual selection
            st.markdown("**Or manually select columns to remove:**")
            
            manual_remove = st.multiselect(
                "Select columns to remove",
                df.columns.tolist()
            )
            
            if manual_remove:
                if st.button("🗑️ Remove Selected Columns", type="primary"):
                    st.session_state.history.add_operation("Remove Selected Columns", df.copy())
                    st.session_state.data = df.drop(columns=manual_remove)
                    st.success(f"✓ Removed {len(manual_remove)} columns!")
                    st.rerun()
        
        with cleaning_tabs[3]:
            st.subheader("Text Cleaning Operations")
            
            # Select text columns
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if not text_cols:
                st.info("No text columns found in dataset")
            else:
                selected_cols = st.multiselect(
                    "Select columns to clean",
                    text_cols,
                    default=text_cols[:min(3, len(text_cols))]
                )
                
                if selected_cols:
                    st.markdown("**Cleaning operations:**")
                    
                    operations = {
                        "Remove extra whitespace": st.checkbox("Remove extra whitespace", value=True),
                        "Convert to lowercase": st.checkbox("Convert to lowercase"),
                        "Remove special characters": st.checkbox("Remove special characters"),
                        "Remove numbers": st.checkbox("Remove numbers"),
                        "Strip whitespace": st.checkbox("Strip leading/trailing whitespace", value=True)
                    }
                    
                    if st.button("🔤 Apply Text Cleaning", type="primary"):
                        st.session_state.history.add_operation("Text Cleaning", df.copy())
                        
                        cleaned_df = cleaner.clean_text_columns(df, selected_cols, operations)
                        st.session_state.data = cleaned_df
                        
                        st.success(f"✓ Cleaned {len(selected_cols)} text columns!")
                        st.rerun()
        
        with cleaning_tabs[4]:
            st.subheader("Data Type Conversion")
            
            col_to_convert = st.selectbox(
                "Select column to convert",
                df.columns.tolist()
            )
            
            if col_to_convert:
                current_type = df[col_to_convert].dtype
                st.info(f"Current type: **{current_type}**")
                
                target_type = st.selectbox(
                    "Convert to",
                    ["int64", "float64", "object", "datetime64", "bool", "category"]
                )
                
                # Preview conversion
                st.markdown("**Preview (first 5 values):**")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("*Before:*")
                    st.write(df[col_to_convert].head())
                
                with col2:
                    st.markdown("*After:*")
                    try:
                        if target_type == "datetime64":
                            preview = pd.to_datetime(df[col_to_convert], errors='coerce').head()
                        elif target_type == "category":
                            preview = df[col_to_convert].astype('category').head()
                        else:
                            preview = df[col_to_convert].astype(target_type).head()
                        st.write(preview)
                    except Exception as e:
                        st.error(f"Cannot convert: {str(e)}")
                        preview = None
                
                if preview is not None:
                    if st.button("🔄 Apply Conversion", type="primary"):
                        try:
                            st.session_state.history.add_operation("Type Conversion", df.copy())
                            
                            if target_type == "datetime64":
                                st.session_state.data[col_to_convert] = pd.to_datetime(
                                    df[col_to_convert], errors='coerce'
                                )
                            elif target_type == "category":
                                st.session_state.data[col_to_convert] = df[col_to_convert].astype('category')
                            else:
                                st.session_state.data[col_to_convert] = df[col_to_convert].astype(target_type)
                            
                            st.success(f"✓ Converted {col_to_convert} to {target_type}!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error converting column: {str(e)}")

elif selected_page == "Missing Values":
    scroll_to_top()
    st.title("❓ Missing Value Imputation")
    
    if st.session_state.data is None:
        st.warning("No data loaded. Please upload a file first.")
    else:
        df = st.session_state.data
        imputer = MissingValueImputer()
        
        # Missing values overview
        missing_info = df.isnull().sum()
        cols_with_missing = missing_info[missing_info > 0]
        
        if len(cols_with_missing) == 0:
            st.success("✓ No missing values in the dataset!")
        else:
            st.warning(f"⚠️ Found missing values in {len(cols_with_missing)} columns")
            
            # Display missing values summary
            col1, col2 = st.columns([2, 1])
            
            with col1:
                missing_df = pd.DataFrame({
                    'Column': cols_with_missing.index,
                    'Missing Count': cols_with_missing.values,
                    'Percentage': (cols_with_missing.values / len(df) * 100).round(2)
                })
                st.dataframe(missing_df, use_container_width=True, height=300)
            
            with col2:
                total_missing = cols_with_missing.sum()
                missing_pct = (total_missing / (len(df) * len(df.columns))) * 100
                
                st.metric("Total Missing", f"{total_missing:,}")
                st.metric("Overall %", f"{missing_pct:.2f}%")
            
            st.markdown("---")
            
            # Imputation methods
            st.subheader("🔧 Imputation Methods")
            
            selected_column = st.selectbox(
                "Select column to impute",
                cols_with_missing.index.tolist()
            )
            
            if selected_column:
                col_dtype = df[selected_column].dtype
                missing_count = df[selected_column].isnull().sum()
                
                st.info(f"**{selected_column}** | Type: {col_dtype} | Missing: {missing_count} ({missing_count/len(df)*100:.1f}%)")
                
                # Method selection based on data type
                if pd.api.types.is_numeric_dtype(df[selected_column]):
                    method_options = [
                        "Mean",
                        "Median",
                        "Mode",
                        "Forward Fill",
                        "Backward Fill",
                        "KNN Imputation (ML)",
                        "Interpolate",
                        "Constant Value"
                    ]
                else:
                    method_options = [
                        "Mode",
                        "Forward Fill",
                        "Backward Fill",
                        "Constant Value"
                    ]
                
                method = st.selectbox("Imputation Method", method_options)
                
                # Method-specific parameters
                params = {}
                
                if method == "KNN Imputation (ML)":
                    params['n_neighbors'] = st.slider("Number of neighbors", 3, 10, 5)
                    st.info("💡 KNN uses similar rows to estimate missing values")
                
                elif method == "Interpolate":
                    params['method'] = st.selectbox(
                        "Interpolation method",
                        ['linear', 'polynomial', 'spline']
                    )
                    if params['method'] in ['polynomial', 'spline']:
                        params['order'] = st.slider("Order", 2, 5, 2)
                
                elif method == "Constant Value":
                    if pd.api.types.is_numeric_dtype(df[selected_column]):
                        params['value'] = st.number_input("Constant value", value=0.0)
                    else:
                        params['value'] = st.text_input("Constant value", value="Unknown")
                
                # Preview imputation
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Before Imputation:**")
                    st.write(df[selected_column].head(10))
                
                with col2:
                    st.markdown("**After Imputation (Preview):**")
                    try:
                        preview_df = imputer.impute_column(df.copy(), selected_column, method, **params)
                        st.write(preview_df[selected_column].head(10))
                        show_apply = True
                    except Exception as e:
                        st.error(f"Cannot preview: {str(e)}")
                        show_apply = False
                
                if show_apply:
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        if st.button("✓ Apply Imputation", type="primary", use_container_width=True):
                            st.session_state.history.add_operation(f"Impute {selected_column}", df.copy())
                            st.session_state.data = imputer.impute_column(df, selected_column, method, **params)
                            st.success(f"✓ Imputed {missing_count} missing values in {selected_column}!")
                            st.rerun()
                    
                    with col2:
                        if st.button("🗑️ Drop Rows", use_container_width=True):
                            st.session_state.history.add_operation(f"Drop missing {selected_column}", df.copy())
                            st.session_state.data = df.dropna(subset=[selected_column])
                            st.success(f"✓ Dropped {missing_count} rows!")
                            st.rerun()
                    
                    with col3:
                        if st.button("🗑️ Drop Column", use_container_width=True):
                            st.session_state.history.add_operation(f"Drop column {selected_column}", df.copy())
                            st.session_state.data = df.drop(columns=[selected_column])
                            st.success(f"✓ Dropped column {selected_column}!")
                            st.rerun()

elif selected_page == "Outlier Detection":
    scroll_to_top()
    st.title("🎯 Outlier Detection & Removal")
    
    if st.session_state.data is None:
        st.warning("No data loaded. Please upload a file first.")
    else:
        df = st.session_state.data
        
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            st.info("No numeric columns found for outlier detection")
        else:
            st.markdown("### Select Column for Outlier Analysis")
            
            selected_column = st.selectbox(
                "Choose a numeric column",
                numeric_cols
            )
            
            if selected_column:
                # Detection method
                method = st.radio(
                    "Detection Method",
                    ["IQR (Interquartile Range)", "Z-Score", "Isolation Forest (ML)"],
                    help="Different methods for detecting outliers"
                )
                
                # Method-specific parameters
                if method == "IQR (Interquartile Range)":
                    threshold = st.slider("IQR Multiplier", 1.0, 3.0, 1.5, 0.1)
                    params = {'method': 'iqr', 'threshold': threshold}
                    st.info("💡 IQR method: Values outside Q1-1.5*IQR to Q3+1.5*IQR are outliers")
                
                elif method == "Z-Score":
                    threshold = st.slider("Z-Score Threshold", 2.0, 4.0, 3.0, 0.1)
                    params = {'method': 'zscore', 'threshold': threshold}
                    st.info("💡 Z-Score: Values with |z-score| > threshold are outliers")
                
                else:  # Isolation Forest
                    contamination = st.slider("Contamination", 0.01, 0.3, 0.1, 0.01)
                    params = {'method': 'isolation_forest', 'contamination': contamination}
                    st.info("💡 Isolation Forest: ML algorithm that identifies anomalies")
                
                # Detect outliers
                from operations.cleaning import DataCleaner
                cleaner = DataCleaner()
                
                try:
                    outliers_mask = cleaner.detect_outliers(df, selected_column, **params)
                    outlier_count = outliers_mask.sum()
                    
                    st.markdown("---")
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Values", len(df))
                    
                    with col2:
                        st.metric("Outliers Detected", outlier_count)
                    
                    with col3:
                        outlier_pct = (outlier_count / len(df)) * 100
                        st.metric("Percentage", f"{outlier_pct:.2f}%")
                    
                    if outlier_count > 0:
                        # Visualization
                        import plotly.express as px
                        import plotly.graph_objects as go
                        
                        fig = go.Figure()
                        
                        # Normal values
                        fig.add_trace(go.Box(
                            y=df[~outliers_mask][selected_column],
                            name="Normal",
                            marker_color='lightblue'
                        ))
                        
                        # Outliers
                        fig.add_trace(go.Scatter(
                            y=df[outliers_mask][selected_column],
                            mode='markers',
                            name="Outliers",
                            marker=dict(color='red', size=8, symbol='x')
                        ))
                        
                        fig.update_layout(
                            title=f"Outlier Detection: {selected_column}",
                            yaxis_title=selected_column,
                            showlegend=True,
                            height=400
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Actions
                        st.markdown("### 🔧 Handle Outliers")
                        
                        action = st.radio(
                            "Choose action",
                            ["Remove outliers", "Cap outliers (winsorize)", "View only"]
                        )
                        
                        if action != "View only":
                            if st.button(f"✓ Apply: {action}", type="primary"):
                                st.session_state.history.add_operation(f"Outlier {action}", df.copy())
                                
                                if action == "Remove outliers":
                                    st.session_state.data = df[~outliers_mask]
                                    st.success(f"✓ Removed {outlier_count} outliers!")
                                
                                elif action == "Cap outliers (winsorize)":
                                    # Cap at percentiles
                                    q1 = df[selected_column].quantile(0.01)
                                    q99 = df[selected_column].quantile(0.99)
                                    st.session_state.data[selected_column] = df[selected_column].clip(q1, q99)
                                    st.success(f"✓ Capped outliers at 1st and 99th percentiles!")
                                
                                st.rerun()
                    
                    else:
                        st.success("✓ No outliers detected!")
                
                except Exception as e:
                    st.error(f"Error detecting outliers: {str(e)}")

elif selected_page == "Encoding":
    scroll_to_top()
    st.title("🔤 Categorical Encoding")
    
    if st.session_state.data is None:
        st.warning("No data loaded. Please upload a file first.")
    else:
        df = st.session_state.data
        encoder = CategoricalEncoder()
        
        # Get categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if not categorical_cols:
            st.info("No categorical columns found in dataset")
        else:
            st.markdown("### Available Categorical Columns")
            st.write(categorical_cols)
            
            st.markdown("---")
            
            # Encoding tabs
            encoding_tabs = st.tabs([
                "🏷️ Label Encoding",
                "🎯 One-Hot Encoding",
                "📊 Ordinal Encoding"
            ])
            
            with encoding_tabs[0]:
                st.subheader("Label Encoding")
                st.markdown("""
                **Label Encoding** converts categories to numbers (0, 1, 2, ...).
                
                - Best for: Tree-based models, categories with many unique values
                - Example: ['Red', 'Blue', 'Green'] → [0, 1, 2]
                """)
                
                label_col = st.selectbox(
                    "Select column for label encoding",
                    categorical_cols,
                    key="label_col"
                )
                
                if label_col:
                    unique_vals = df[label_col].nunique()
                    st.info(f"**{label_col}** has {unique_vals} unique values")
                    
                    # Preview
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Original Values:**")
                        st.write(df[label_col].value_counts().head(10))
                    
                    with col2:
                        st.markdown("**After Encoding (Preview):**")
                        preview = encoder.label_encode(df.copy(), label_col)
                        st.write(preview[label_col].head(10))
                    
                    if st.button("✓ Apply Label Encoding", type="primary", key="apply_label"):
                        st.session_state.history.add_operation(f"Label Encode {label_col}", df.copy())
                        st.session_state.data = encoder.label_encode(df, label_col)
                        st.success(f"✓ Applied label encoding to {label_col}!")
                        st.rerun()
            
            with encoding_tabs[1]:
                st.subheader("One-Hot Encoding")
                st.markdown("""
                **One-Hot Encoding** creates binary columns for each category.
                
                - Best for: Linear models, categories with few unique values
                - Example: ['Red', 'Blue'] → [Red: 1, Blue: 0] or [Red: 0, Blue: 1]
                """)
                
                onehot_cols = st.multiselect(
                    "Select columns for one-hot encoding",
                    categorical_cols,
                    key="onehot_cols"
                )
                
                if onehot_cols:
                    # Preview
                    total_new_cols = sum([df[col].nunique() for col in onehot_cols])
                    st.warning(f"⚠️ This will create {total_new_cols} new columns")
                    
                    drop_first = st.checkbox(
                        "Drop first category (avoid multicollinearity)",
                        value=True,
                        help="Recommended for linear models"
                    )
                    
                    if st.button("✓ Apply One-Hot Encoding", type="primary", key="apply_onehot"):
                        st.session_state.history.add_operation(f"One-Hot Encode {onehot_cols}", df.copy())
                        st.session_state.data = encoder.onehot_encode(df, onehot_cols, drop_first=drop_first)
                        st.success(f"✓ Applied one-hot encoding to {len(onehot_cols)} columns!")
                        st.rerun()
            
            with encoding_tabs[2]:
                st.subheader("Ordinal Encoding")
                st.markdown("""
                **Ordinal Encoding** maps categories to numbers with custom order.
                
                - Best for: Ordered categories (e.g., Low < Medium < High)
                - You define the order and mapping
                """)
                
                ordinal_col = st.selectbox(
                    "Select column for ordinal encoding",
                    categorical_cols,
                    key="ordinal_col"
                )
                
                if ordinal_col:
                    unique_values = df[ordinal_col].unique().tolist()
                    st.info(f"Found {len(unique_values)} unique values")
                    
                    st.markdown("**Define the order (drag or reorder):**")
                    
                    # Let user define order
                    ordered_values = st.multiselect(
                        "Select values in order (low to high)",
                        unique_values,
                        default=unique_values[:min(5, len(unique_values))]
                    )
                    
                    if ordered_values:
                        # Show mapping
                        st.markdown("**Mapping:**")
                        mapping_df = pd.DataFrame({
                            'Category': ordered_values,
                            'Encoded Value': list(range(len(ordered_values)))
                        })
                        st.dataframe(mapping_df)
                        
                        if len(ordered_values) == len(unique_values):
                            if st.button("✓ Apply Ordinal Encoding", type="primary", key="apply_ordinal"):
                                mapping = {cat: i for i, cat in enumerate(ordered_values)}
                                st.session_state.history.add_operation(f"Ordinal Encode {ordinal_col}", df.copy())
                                st.session_state.data = encoder.ordinal_encode(df, ordinal_col, mapping)
                                st.success(f"✓ Applied ordinal encoding to {ordinal_col}!")
                                st.rerun()
                        else:
                            st.warning("Please select all unique values in order")

elif selected_page == "Visualization":
    scroll_to_top()
    st.title("📈 Data Visualization")
    
    if st.session_state.data is None:
        st.warning("No data loaded. Please upload a file first.")
    else:
        df = st.session_state.data
        chart_gen = ChartGenerator()
        
        # Visualization type selection
        viz_type = st.selectbox(
            "Select Visualization Type",
            [
                "Histogram",
                "Box Plot",
                "Scatter Plot",
                "Line Chart",
                "Bar Chart",
                "Correlation Heatmap",
                "Distribution Plot",
                "Pair Plot"
            ]
        )
        
        st.markdown("---")
        
        if viz_type == "Histogram":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                col = st.selectbox("Select column", numeric_cols)
                bins = st.slider("Number of bins", 10, 100, 30)
                
                if col:
                    fig = chart_gen.create_histogram(df, col, bins)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns available")
        
        elif viz_type == "Box Plot":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                col = st.selectbox("Select column", numeric_cols)
                
                # Optional grouping
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                group_by = None
                
                if categorical_cols:
                    use_grouping = st.checkbox("Group by category")
                    if use_grouping:
                        group_by = st.selectbox("Group by", categorical_cols)
                
                if col:
                    fig = chart_gen.create_boxplot(df, col, group_by)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns available")
        
        elif viz_type == "Scatter Plot":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("X-axis", numeric_cols, index=0)
                
                with col2:
                    y_col = st.selectbox("Y-axis", numeric_cols, index=min(1, len(numeric_cols)-1))
                
                # Optional color grouping
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                color_by = None
                
                if categorical_cols:
                    use_color = st.checkbox("Color by category")
                    if use_color:
                        color_by = st.selectbox("Color by", categorical_cols)
                
                if x_col and y_col:
                    fig = chart_gen.create_scatter(df, x_col, y_col, color_by)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least 2 numeric columns")
        
        elif viz_type == "Line Chart":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                y_cols = st.multiselect("Select columns to plot", numeric_cols, default=numeric_cols[:min(3, len(numeric_cols))])
                
                # Optional x-axis
                x_col = st.selectbox("X-axis (optional - uses index if not selected)", [None] + df.columns.tolist())
                
                if y_cols:
                    fig = chart_gen.create_line_chart(df, y_cols, x_col)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns available")
        
        elif viz_type == "Bar Chart":
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if categorical_cols:
                col1, col2 = st.columns(2)
                
                with col1:
                    x_col = st.selectbox("Category column", categorical_cols)
                
                with col2:
                    agg_func = st.selectbox("Aggregation", ["count", "sum", "mean", "median"])
                
                y_col = None
                if agg_func != "count" and numeric_cols:
                    y_col = st.selectbox("Value column", numeric_cols)
                
                if x_col:
                    fig = chart_gen.create_bar_chart(df, x_col, y_col, agg_func)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No categorical columns available")
        
        elif viz_type == "Correlation Heatmap":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                selected_cols = st.multiselect(
                    "Select columns (leave empty for all)",
                    numeric_cols,
                    default=[]
                )
                
                cols_to_use = selected_cols if selected_cols else numeric_cols
                
                if len(cols_to_use) >= 2:
                    fig = chart_gen.create_correlation_heatmap(df[cols_to_use])
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least 2 numeric columns")
        
        elif viz_type == "Distribution Plot":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if numeric_cols:
                col = st.selectbox("Select column", numeric_cols)
                
                if col:
                    fig = chart_gen.create_distribution_plot(df, col)
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns available")
        
        elif viz_type == "Pair Plot":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                selected_cols = st.multiselect(
                    "Select columns (max 5 recommended)",
                    numeric_cols,
                    default=numeric_cols[:min(3, len(numeric_cols))]
                )
                
                if len(selected_cols) >= 2:
                    if len(selected_cols) > 5:
                        st.warning("⚠️ Large pair plots may be slow. Consider selecting fewer columns.")
                    
                    fig = chart_gen.create_pair_plot(df[selected_cols])
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Need at least 2 numeric columns")

elif selected_page == "Export":
    scroll_to_top()
    st.title("💾 Export Data")
    
    if st.session_state.data is None:
        st.warning("No data loaded. Please upload a file first.")
    else:
        df = st.session_state.data
        
        st.subheader("📊 Data Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Rows", f"{len(df):,}")
        
        with col2:
            st.metric("Columns", len(df.columns))
        
        with col3:
            missing = df.isnull().sum().sum()
            st.metric("Missing Values", f"{missing:,}")
        
        with col4:
            if st.session_state.original_data is not None:
                original_rows = len(st.session_state.original_data)
                cleaned_rows = len(df)
                diff = original_rows - cleaned_rows
                st.metric("Rows Removed", f"{diff:,}")
        
        st.markdown("---")
        
        # Export options
        st.subheader("⚙️ Export Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            export_format = st.selectbox(
                "Export Format",
                ["CSV", "Excel", "JSON"],
                help="Choose the output file format"
            )
        
        with col2:
            if export_format in ["CSV"]:
                export_encoding = st.selectbox(
                    "Encoding",
                    ["UTF-8", "Latin-1", "ISO-8859-1", "Windows-1252"],
                    help="Character encoding for the file"
                )
            else:
                export_encoding = "UTF-8"
        
        # Additional options - Initialize default values
        separator = ","
        include_index = False
        sheet_name = "Sheet1"
        orient = "records"
        
        if export_format == "CSV":
            col1, col2 = st.columns(2)
            
            with col1:
                separator = st.selectbox("Separator", [",", ";", "\t", "|"], index=0)
            
            with col2:
                include_index = st.checkbox("Include row index", value=False)
        
        elif export_format == "Excel":
            sheet_name = st.text_input("Sheet name", value="Sheet1")
            include_index = st.checkbox("Include row index", value=False)
        
        elif export_format == "JSON":
            orient = st.selectbox(
                "JSON orientation",
                ["records", "split", "index", "columns", "values"],
                help="How to structure the JSON output"
            )
        
        # Preview
        st.markdown("---")
        st.subheader("👁️ Preview (First 10 Rows)")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Export button
        st.markdown("---")
        
        if st.button("📥 Download Data", type="primary", use_container_width=True):
            try:
                # Prepare file - Initialize file_ext and mime_type
                buffer = io.BytesIO()
                file_ext = "csv"
                mime_type = "text/csv"
                
                if export_format == "CSV":
                    csv_data = df.to_csv(
                        index=include_index,
                        sep=separator,
                        encoding=export_encoding
                    )
                    buffer.write(csv_data.encode(export_encoding))
                    file_ext = "csv"
                    mime_type = "text/csv"
                
                elif export_format == "Excel":
                    df.to_excel(buffer, index=include_index, sheet_name=sheet_name, engine='openpyxl')
                    file_ext = "xlsx"
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                elif export_format == "JSON":
                    json_data = df.to_json(orient=orient, indent=2)
                    buffer.write(json_data.encode('utf-8'))
                    file_ext = "json"
                    mime_type = "application/json"
                
                buffer.seek(0)
                
                # Generate filename
                timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
                filename = f"cleaned_data_{timestamp}.{file_ext}"
                
                st.download_button(
                    label=f"💾 Download {export_format}",
                    data=buffer,
                    file_name=filename,
                    mime=mime_type,
                    use_container_width=True
                )
                
                st.success(f"✓ File ready for download: {filename}")
                
            except Exception as e:
                st.error(f"❌ Error creating export file: {str(e)}")
        
        # Operation history
        if len(st.session_state.history.history) > 0:
            st.markdown("---")
            st.subheader("📋 Cleaning History")
            
            history_df = pd.DataFrame([
                {
                    'Step': i + 1,
                    'Operation': op['operation'],
                    'Timestamp': op['timestamp']
                }
                for i, op in enumerate(st.session_state.history.history)
            ])
            
            st.dataframe(history_df, use_container_width=True, hide_index=True)

elif selected_page == "Help":
    scroll_to_top()
    st.title("❓ Help & Documentation")
    
    # Help tabs
    help_tabs = st.tabs([
        "📖 Getting Started",
        "🔧 Features",
        "💡 Tips & Tricks",
        "🐛 Troubleshooting"
    ])
    
    with help_tabs[0]:
        st.markdown("""
        ## Getting Started with Datalix
        
        ### 1. Upload Your Data
        - Navigate to **Data Upload** in the sidebar
        - Choose your file (CSV, Excel, JSON, or Parquet)
        - Select encoding or use auto-detection
        - Click **Load Data**
        
        ### 2. Explore Your Data
        - Go to **Data Preview** to see your data
        - Check **Data Profiling** for quality insights
        - Review the quality score and recommendations
        
        ### 3. Clean Your Data
        - Use **Data Cleaning** for basic operations
        - Handle **Missing Values** with various methods
        - Detect and remove **Outliers**
        - Apply **Encoding** to categorical variables
        
        ### 4. Visualize & Export
        - Create charts in **Visualization**
        - Export your cleaned data in **Export**
        
        ### Supported File Formats
        - **CSV** (.csv, .tsv, .txt)
        - **Excel** (.xlsx, .xls)
        - **JSON** (.json)
        - **Parquet** (.parquet)
        
        ### File Size Limits
        - Maximum file size: **200MB**
        - Instant preview: First **1000 rows**
        - Full processing with chunking for larger files
        """)
    
    with help_tabs[1]:
        st.markdown("""
        ## Feature Guide
        
        ### 📁 Data Upload
        - **Auto-encoding detection**: Automatically detects file encoding
        - **Multiple formats**: Support for CSV, Excel, JSON, Parquet
        - **URL import**: Load data directly from URLs
        - **Sample datasets**: Try with built-in examples
        
        ### 🧹 Data Cleaning
        - **Auto-clean**: One-click automated cleaning
        - **Remove duplicates**: Keep first or last occurrence
        - **Text cleaning**: Standardize and clean text columns
        - **Type conversion**: Convert between data types
        
        ### ❓ Missing Value Handling
        - **Mean/Median/Mode**: Statistical imputation
        - **KNN Imputation**: ML-based estimation
        - **Forward/Backward Fill**: Use adjacent values
        - **Interpolation**: Linear, polynomial, or spline
        
        ### 🎯 Outlier Detection
        - **IQR Method**: Statistical approach
        - **Z-Score**: Standard deviation based
        - **Isolation Forest**: ML-based anomaly detection
        
        ### 🔤 Categorical Encoding
        - **Label Encoding**: Convert to numeric labels
        - **One-Hot Encoding**: Create binary columns
        - **Ordinal Encoding**: Custom ordered mapping
        
        ### 📈 Visualization
        - **Histograms**: Distribution analysis
        - **Box Plots**: Outlier visualization
        - **Scatter Plots**: Relationship analysis
        - **Correlation Heatmaps**: Feature relationships
        - **And more...**
        
        ### 💾 Export Options
        - **CSV**: With custom separator and encoding
        - **Excel**: With custom sheet names
        - **JSON**: With multiple orientations
        """)
    
    with help_tabs[2]:
        st.markdown("""
        ## Tips & Tricks
        
        ### 🎯 Best Practices
        
        1. **Always preview first**
           - Check your data in Data Preview before cleaning
           - Review the quality score in Data Profiling
        
        2. **Use auto-clean for quick starts**
           - Auto-clean handles most common issues
           - Review the operations it performed
        
        3. **Handle missing values carefully**
           - Choose the right imputation method for your data
           - KNN works well for numeric data with patterns
           - Forward/backward fill is good for time series
        
        4. **Check for outliers**
           - Always visualize before removing outliers
           - Consider capping instead of removing
           - Different methods may find different outliers
        
        5. **Encoding matters**
           - Use one-hot for linear models
           - Use label encoding for tree-based models
           - Use ordinal encoding for ordered categories
        
        ### ⚡ Performance Tips
        
        - For large files, let the chunked processing complete
        - Use pagination in preview to avoid loading all data
        - Limit visualizations to necessary columns
        - Export early if you need to save intermediate results
        
        ### 🔄 Undo Operations
        
        - All operations are tracked
        - Use the "Undo Last" button in Auto-Clean
        - Operation history is shown in the Export page
        
        ### 📊 Quality Score
        
        The quality score is calculated from:
        - **Completeness (40%)**: Non-missing values
        - **Consistency (30%)**: Formatting uniformity
        - **Uniqueness (20%)**: Duplicate records
        - **Validity (10%)**: Outlier presence
        """)
    
    with help_tabs[3]:
        st.markdown("""
        ## Troubleshooting
        
        ### Common Issues
        
        #### File Won't Load
        - **Check file size**: Must be under 200MB
        - **Try auto-detect encoding**: If you get encoding errors
        - **Verify file format**: Ensure it matches the extension
        
        #### Missing Values Won't Impute
        - **Check data type**: Some methods only work with numeric data
        - **Verify column has missing values**: Select columns with NaN values
        - **Try different method**: Some methods may fail on certain data patterns
        
        #### Encoding Fails
        - **Check unique values**: One-hot encoding needs reasonable cardinality
        - **Verify column type**: Must be categorical or object type
        - **For ordinal**: Ensure you selected all unique values in order
        
        #### Visualization Not Showing
        - **Check data type**: Numeric columns needed for most charts
        - **Verify selection**: Ensure you selected valid columns
        - **Try different chart**: Some charts have specific requirements
        
        #### Export Fails
        - **Check memory**: Very large datasets may cause issues
        - **Try different format**: Some formats handle large data better
        - **Reduce data size**: Export only necessary columns
        
        ### Error Messages
        
        - **"No data loaded"**: Upload a file first
        - **"No numeric columns"**: Operation requires numeric data
        - **"Cannot convert"**: Data type conversion not possible
        - **"Encoding error"**: File encoding doesn't match selected encoding
        
        ### Getting More Help
        
        If you encounter persistent issues:
        1. Check the data preview for any obvious problems
        2. Review the quality score for insights
        3. Try with a sample dataset to verify functionality
        4. Consider simplifying your data or operations
        
        ### Performance Issues
        
        If the app is slow:
        - Reduce the number of rows in preview
        - Limit visualization to fewer columns
        - Use pagination effectively
        - Consider exporting and working with smaller subsets
        """)

# Footer
st.markdown("---")
st.caption("Datalix v2.0.0 - Advanced Data Cleaning Platform | Built with Streamlit")
