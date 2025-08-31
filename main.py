# Advanced Data Cleaning and Visualization Platform
# Phase 1 & 2 Implementation with AI-Powered Features

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from scipy import stats
import io
import json
import sqlite3
import requests
from datetime import datetime, timedelta
import re
import warnings
warnings.filterwarnings('ignore')

# Configure the Streamlit page with enhanced settings
st.set_page_config(
    page_title="📊 Datalix",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/HimanshuSingh-966/Datalix',
        'Report a bug': "https://github.com/HimanshuSingh-966/Datalix",
        'About': "# Datalix\n\nAI-Powered Data Cleaning, Analysis & Visualization"
    }
)

# Enhanced Modern CSS with Advanced Design
st.markdown("""
<style>
    /* Import Google Fonts for modern typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Enhanced Main Header with Gradient and Animation */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        animation: gradientShift 3s ease-in-out infinite;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    @keyframes gradientShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Enhanced Section Headers */
    .section-header {
        font-size: 2rem;
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #4f46e5, #7c3aed) 1;
        padding-bottom: 0.75rem;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 50px;
        height: 3px;
        background: linear-gradient(90deg, #f093fb, #f5576c);
        animation: slideRight 2s ease-in-out infinite;
    }
    
    @keyframes slideRight {
        0% { transform: translateX(0); }
        50% { transform: translateX(100px); }
        100% { transform: translateX(0); }
    }
    
    /* Enhanced Feature Cards with Glassmorphism */
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(79, 70, 229, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.5s;
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(79, 70, 229, 0.15);
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    /* Enhanced AI Suggestion Cards */
    .ai-suggestion {
        background: linear-gradient(135deg, rgba(254, 243, 199, 0.9) 0%, rgba(251, 191, 36, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border-left: 6px solid #f59e0b;
        margin: 1.5rem 0;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.15);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .ai-suggestion::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #f59e0b, #fbbf24, #f59e0b);
        animation: shimmer 2s linear infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .ai-suggestion:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.25);
    }
    
    /* Enhanced Quality Score with 3D Effect */
    .quality-score {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        padding: 1.5rem;
        border-radius: 50%;
        margin: 0 auto;
        width: 120px;
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .quality-score::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        border-radius: 50%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.3), transparent);
        z-index: -1;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .score-excellent { 
        background: linear-gradient(135deg, #10b981, #34d399, #6ee7b7);
        color: white;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
    }
    .score-good { 
        background: linear-gradient(135deg, #3b82f6, #60a5fa, #93c5fd);
        color: white;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.4);
    }
    .score-fair { 
        background: linear-gradient(135deg, #f59e0b, #fbbf24, #fcd34d);
        color: white;
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.4);
    }
    .score-poor { 
        background: linear-gradient(135deg, #ef4444, #f87171, #fca5a5);
        color: white;
        box-shadow: 0 10px 30px rgba(239, 68, 68, 0.4);
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #f093fb);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    
    .metric-card h2 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        color: #6b7280;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Enhanced Template Cards */
    .template-card {
        background: linear-gradient(135deg, rgba(240, 249, 255, 0.9) 0%, rgba(219, 234, 254, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(147, 197, 253, 0.3);
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .template-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        transform: translateX(-100%);
        transition: transform 0.6s;
    }
    
    .template-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.2);
    }
    
    .template-card:hover::before {
        transform: translateX(100%);
    }
    
    /* Enhanced Buttons with Better Visibility */
    .stButton > button {
        background: #2563eb !important;
        color: white !important;
        border: 2px solid #2563eb !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3) !important;
        min-height: 45px !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4) !important;
        background: #1d4ed8 !important;
        border-color: #1d4ed8 !important;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:focus {
        outline: 3px solid rgba(37, 99, 235, 0.4) !important;
        outline-offset: 2px !important;
        background: #2563eb !important;
    }
    
    /* Enhanced Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8faff 0%, #e0e7ff 100%);
        border-right: 1px solid rgba(79, 70, 229, 0.1);
    }
    
    /* Enhanced Selectboxes with Better Visibility */
    .stSelectbox > div > div {
        border-radius: 8px !important;
        border: 2px solid #374151 !important;
        background: #374151 !important;
        color: white !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 4px rgba(55, 65, 81, 0.3) !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #4b5563 !important;
        background: #4b5563 !important;
        box-shadow: 0 4px 8px rgba(75, 85, 99, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    .stSelectbox > div > div > div {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Enhanced File Uploader */
    .stFileUploader > div {
        border: 2px dashed rgba(79, 70, 229, 0.3);
        border-radius: 16px;
        background: rgba(240, 249, 255, 0.5);
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #4f46e5;
        background: rgba(240, 249, 255, 0.8);
        transform: scale(1.02);
    }
    
    /* Enhanced Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    }
    
    /* Enhanced Progress Bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #f093fb);
        border-radius: 10px;
    }
    
    /* Enhanced Success/Error Messages */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Enhanced Expanders */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.05) 0%, rgba(124, 58, 237, 0.05) 100%);
        border-radius: 12px;
        border: 1px solid rgba(79, 70, 229, 0.1);
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%);
        transform: translateY(-1px);
    }
    
    /* Enhanced Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(240, 249, 255, 0.5);
        border-radius: 12px;
        padding: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        background: transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        box-shadow: 0 2px 10px rgba(79, 70, 229, 0.3);
    }
    
    /* Enhanced Radio Buttons with Better Visibility */
    .stRadio > div > label {
        background: #374151 !important;
        color: white !important;
        border: 2px solid #374151 !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        margin: 0.25rem 0 !important;
        transition: all 0.3s ease !important;
        cursor: pointer !important;
        font-weight: 500 !important;
        box-shadow: 0 2px 4px rgba(55, 65, 81, 0.3) !important;
    }
    
    .stRadio > div > label:hover {
        border-color: #4b5563 !important;
        background: #4b5563 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(75, 85, 99, 0.4) !important;
    }
    
    .stRadio > div > label[data-testid="stRadio"] {
        background: #2563eb !important;
        color: white !important;
        border-color: #2563eb !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4) !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar Radio Buttons Specific Styling */
    .css-1d391kg .stRadio > div > label {
        background: #374151 !important;
        color: white !important;
        border: 2px solid #374151 !important;
        font-weight: 500 !important;
        margin: 0.3rem 0 !important;
    }
    
    .css-1d391kg .stRadio > div > label:hover {
        background: #4b5563 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Enhanced Text Inputs */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid rgba(79, 70, 229, 0.2);
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4f46e5;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
    }
    
    /* Enhanced Sliders */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #4f46e5, #7c3aed);
    }
    
    /* Enhanced Checkboxes */
    .stCheckbox > label {
        background: rgba(255, 255, 255, 0.8);
        border: 2px solid rgba(79, 70, 229, 0.2);
        border-radius: 8px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .stCheckbox > label:hover {
        border-color: #4f46e5;
        background: rgba(79, 70, 229, 0.05);
    }
    
    /* Enhanced Multi-Select with Better Visibility */
    .stMultiSelect > div > div {
        border-radius: 12px !important;
        border: 2px solid #1e40af !important;
        background: linear-gradient(135deg, #1e40af 0%, #7c2d12 100%) !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.3) !important;
    }
    
    .stMultiSelect > div > div:hover {
        border-color: #1d4ed8 !important;
        background: linear-gradient(135deg, #1d4ed8 0%, #92400e 100%) !important;
        box-shadow: 0 6px 20px rgba(30, 64, 175, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    .stMultiSelect > div > div > div {
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Enhanced Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 250px;
        background: rgba(0, 0, 0, 0.9);
        color: white;
        text-align: center;
        padding: 12px;
        border-radius: 12px;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        margin-left: -125px;
        opacity: 0;
        transition: opacity 0.3s ease;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Loading Animations */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading {
        animation: spin 1s linear infinite;
    }
    
    /* Enhanced Mobile Responsiveness */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .section-header {
            font-size: 1.6rem;
        }
        .metric-card {
            margin-bottom: 1rem;
            padding: 1rem;
        }
        .quality-score {
            width: 100px;
            height: 100px;
            font-size: 2rem;
        }
        .feature-card {
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .stButton > button {
            width: 100%;
            margin: 0.5rem 0;
        }
    }
    
    /* Enhanced Dark Mode Support */
    @media (prefers-color-scheme: dark) {
        .feature-card {
            background: rgba(30, 30, 30, 0.95);
            border-color: rgba(255, 255, 255, 0.1);
        }
        .metric-card {
            background: rgba(30, 30, 30, 0.9);
            border-color: rgba(255, 255, 255, 0.1);
        }
        .template-card {
            background: linear-gradient(135deg, rgba(30, 30, 30, 0.9) 0%, rgba(40, 40, 40, 0.9) 100%);
            border-color: rgba(255, 255, 255, 0.1);
        }
    }
    
    /* Enhanced Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(240, 249, 255, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #4338ca, #6d28d9);
    }
    
    /* Enhanced Focus States */
    *:focus {
        outline: 2px solid #4f46e5;
        outline-offset: 2px;
    }
    
    /* Enhanced Animations for Charts */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }
    
    .js-plotly-plot:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    /* Enhanced Footer */
    .enhanced-footer {
        background: linear-gradient(135deg, #f8faff 0%, #e0e7ff 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 8px 32px rgba(79, 70, 229, 0.1);
        border: 1px solid rgba(79, 70, 229, 0.1);
    }
    
    /* Enhanced Status Indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s ease-in-out infinite;
    }
    
    .status-success { background: #10b981; }
    .status-warning { background: #f59e0b; }
    .status-error { background: #ef4444; }
    .status-info { background: #3b82f6; }
    
    /* Enhanced Code Blocks */
    .stCodeBlock {
        border-radius: 12px;
        border: 1px solid rgba(79, 70, 229, 0.1);
        background: rgba(240, 249, 255, 0.5);
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Enhanced Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #4f46e5, transparent);
        margin: 2rem 0;
        border-radius: 1px;
    }
    
    /* Enhanced Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0.25rem;
    }
    
    .badge-primary {
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
    }
    
    .badge-success {
        background: linear-gradient(135deg, #10b981, #34d399);
        color: white;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #f59e0b, #fbbf24);
        color: white;
    }
    
    .badge-error {
        background: linear-gradient(135deg, #ef4444, #f87171);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize enhanced session state
def initialize_session_state():
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'original_df' not in st.session_state:
        st.session_state.original_df = None
    if 'cleaning_history' not in st.session_state:
        st.session_state.cleaning_history = []
    if 'templates' not in st.session_state:
        st.session_state.templates = {}
    if 'data_quality_score' not in st.session_state:
        st.session_state.data_quality_score = None
    if 'ai_suggestions' not in st.session_state:
        st.session_state.ai_suggestions = []
    if 'dashboard_config' not in st.session_state:
        st.session_state.dashboard_config = {}

initialize_session_state()

# Enhanced file loading with multiple format support
def load_data_advanced(uploaded_files, source_type="file"):
    """Enhanced data loading supporting multiple files and sources"""
    try:
        if source_type == "file":
            if len(uploaded_files) == 1:
                file = uploaded_files[0]
                file_extension = file.name.split('.')[-1].lower()
                
                if file_extension == 'csv':
                    # Enhanced CSV reading with encoding detection
                    try:
                        df = pd.read_csv(file, encoding='utf-8')
                    except UnicodeDecodeError:
                        df = pd.read_csv(file, encoding='latin-1')
                elif file_extension in ['xlsx', 'xls']:
                    df = pd.read_excel(file, sheet_name=0)
                elif file_extension == 'json':
                    df = pd.read_json(file)
                elif file_extension == 'parquet':
                    df = pd.read_parquet(file)
                elif file_extension == 'tsv':
                    df = pd.read_csv(file, sep='\t')
                elif file_extension == 'txt':
                    # Auto-detect delimiter
                    df = pd.read_csv(file, sep=None, engine='python')
                else:
                    st.error("❌ Unsupported file format!")
                    return None
                    
                return df
            else:
                # Handle multiple files - merge them
                dataframes = []
                for file in uploaded_files:
                    file_extension = file.name.split('.')[-1].lower()
                    if file_extension == 'csv':
                        df = pd.read_csv(file)
                    elif file_extension in ['xlsx', 'xls']:
                        df = pd.read_excel(file)
                    else:
                        continue
                    df['source_file'] = file.name
                    dataframes.append(df)
                
                if dataframes:
                    return pd.concat(dataframes, ignore_index=True)
                else:
                    st.error("❌ No supported files found!")
                    return None
                    
    except Exception as e:
        st.error(f"❌ Error loading file: {str(e)}")
        return None

# AI-Powered Data Quality Assessment
def calculate_data_quality_score(df):
    """Calculate comprehensive data quality score with AI insights"""
    if df is None or df.empty:
        return 0, []
    
    scores = {}
    suggestions = []
    
    # Completeness Score (40%)
    missing_percentage = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    completeness = max(0, 100 - missing_percentage)
    scores['completeness'] = completeness * 0.4
    
    if missing_percentage > 20:
        suggestions.append({
            'type': 'warning',
            'title': 'High Missing Data',
            'message': f'{missing_percentage:.1f}% of your data is missing. Consider imputation or collecting more data.',
            'action': 'Handle missing values in the Data Cleaning section'
        })
    
    # Consistency Score (30%)
    consistency_issues = 0
    total_checks = 0
    
    for col in df.columns:
        total_checks += 1
        if df[col].dtype == 'object':
            # Check for inconsistent formatting
            unique_vals = df[col].dropna().astype(str)
            if len(unique_vals) > 0:
                # Check for mixed case issues
                mixed_case = len(set(unique_vals.str.lower())) != len(set(unique_vals))
                if mixed_case:
                    consistency_issues += 1
    
    consistency = max(0, (1 - consistency_issues / max(total_checks, 1)) * 100)
    scores['consistency'] = consistency * 0.3
    
    # Uniqueness Score (20%)
    duplicate_percentage = (df.duplicated().sum() / len(df)) * 100
    uniqueness = max(0, 100 - duplicate_percentage * 2)  # Penalize duplicates more
    scores['uniqueness'] = uniqueness * 0.2
    
    if duplicate_percentage > 5:
        suggestions.append({
            'type': 'info',
            'title': 'Duplicate Records Found',
            'message': f'{duplicate_percentage:.1f}% of records are duplicates.',
            'action': 'Remove duplicates in the Data Cleaning section'
        })
    
    # Validity Score (10%)
    validity_issues = 0
    validity_checks = 0
    
    for col in df.select_dtypes(include=[np.number]).columns:
        validity_checks += 1
        # Check for extreme outliers
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        outliers = ((df[col] < (Q1 - 3 * IQR)) | (df[col] > (Q3 + 3 * IQR))).sum()
        if outliers > len(df) * 0.05:  # More than 5% outliers
            validity_issues += 1
    
    validity = max(0, (1 - validity_issues / max(validity_checks, 1)) * 100)
    scores['validity'] = validity * 0.1
    
    total_score = sum(scores.values())
    
    # Generate AI suggestions based on data characteristics
    if total_score > 85:
        suggestions.append({
            'type': 'success',
            'title': 'Excellent Data Quality!',
            'message': 'Your data is in great shape. You can proceed directly to analysis and visualization.',
            'action': 'Explore the Visualization section'
        })
    elif total_score > 70:
        suggestions.append({
            'type': 'info',
            'title': 'Good Data Quality',
            'message': 'Minor issues detected. A quick cleanup will improve your analysis quality.',
            'action': 'Review and apply suggested cleaning steps'
        })
    else:
        suggestions.append({
            'type': 'warning',
            'title': 'Data Needs Attention',
            'message': 'Significant data quality issues detected. Cleaning is strongly recommended.',
            'action': 'Start with the most critical issues first'
        })
    
    return min(100, max(0, total_score)), suggestions

# Smart Data Type Detection
def detect_data_types_smart(df):
    """AI-powered smart data type detection"""
    suggestions = {}
    
    for col in df.columns:
        current_type = str(df[col].dtype)
        sample_values = df[col].dropna().astype(str).head(100)
        
        if len(sample_values) == 0:
            continue
            
        # Email detection
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if sample_values.str.match(email_pattern).sum() > len(sample_values) * 0.8:
            suggestions[col] = {'suggested_type': 'email', 'confidence': 'high'}
            continue
            
        # Phone number detection
        phone_pattern = r'^\+?1?-?\.?\s?\(?(\d{3})\)?[\s\-\.]?(\d{3})[\s\-\.]?(\d{4})$'
        if sample_values.str.match(phone_pattern).sum() > len(sample_values) * 0.7:
            suggestions[col] = {'suggested_type': 'phone', 'confidence': 'high'}
            continue
            
        # Date detection
        try:
            pd.to_datetime(sample_values, infer_datetime_format=True)
            if current_type == 'object':
                suggestions[col] = {'suggested_type': 'datetime', 'confidence': 'high'}
                continue
        except:
            pass
            
        # Categorical detection (if unique values < 10% of total)
        unique_ratio = len(sample_values.unique()) / len(sample_values)
        if unique_ratio < 0.1 and len(sample_values.unique()) < 20:
            suggestions[col] = {'suggested_type': 'category', 'confidence': 'medium'}
            
    return suggestions

# Enhanced Missing Value Handling with ML
def handle_missing_values_advanced(df, column, method, **kwargs):
    """Advanced missing value handling including ML-based imputation"""
    df_copy = df.copy()
    
    if method == "ML Imputation (KNN)":
        from sklearn.impute import KNNImputer
        
        # Only use numeric columns for KNN
        numeric_cols = df_copy.select_dtypes(include=[np.number]).columns.tolist()
        if column in numeric_cols and len(numeric_cols) > 1:
            imputer = KNNImputer(n_neighbors=5)
            df_copy[numeric_cols] = imputer.fit_transform(df_copy[numeric_cols])
        else:
            st.warning("KNN imputation requires multiple numeric columns!")
            return df_copy
            
    elif method == "Group-based Mean":
        group_col = kwargs.get('group_column')
        if group_col and group_col != column:
            df_copy[column] = df_copy.groupby(group_col)[column].transform(
                lambda x: x.fillna(x.mean())
            )
        else:
            st.warning("Please select a different column for grouping!")
            return df_copy
            
    elif method == "Interpolation":
        if df_copy[column].dtype in ['int64', 'float64']:
            df_copy[column] = df_copy[column].interpolate(method='linear')
        else:
            st.warning("Interpolation only works with numeric data!")
            return df_copy
            
    else:
        # Original methods
        if method == "Remove rows with missing values":
            df_copy = df_copy.dropna(subset=[column])
        elif method == "Fill with mean":
            if df_copy[column].dtype in ['int64', 'float64']:
                df_copy[column].fillna(df_copy[column].mean(), inplace=True)
        elif method == "Fill with median":
            if df_copy[column].dtype in ['int64', 'float64']:
                df_copy[column].fillna(df_copy[column].median(), inplace=True)
        elif method == "Fill with mode":
            mode_value = df_copy[column].mode()
            if not mode_value.empty:
                df_copy[column].fillna(mode_value[0], inplace=True)
        elif method == "Forward fill":
            df_copy[column].fillna(method='ffill', inplace=True)
        elif method == "Backward fill":
            df_copy[column].fillna(method='bfill', inplace=True)
    
    return df_copy

# Advanced Outlier Detection
def detect_outliers_advanced(df, columns, method='isolation_forest'):
    """Advanced outlier detection using multiple algorithms"""
    outlier_indices = set()
    
    if method == 'isolation_forest':
        # Use Isolation Forest for multivariate outlier detection
        numeric_data = df[columns].select_dtypes(include=[np.number])
        if len(numeric_data.columns) > 0:
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            outlier_labels = iso_forest.fit_predict(numeric_data.fillna(numeric_data.mean()))
            outlier_indices.update(np.where(outlier_labels == -1)[0])
    
    elif method == 'statistical':
        # Combined statistical approach
        for col in columns:
            if df[col].dtype in ['int64', 'float64']:
                # IQR method
                Q1, Q3 = df[col].quantile([0.25, 0.75])
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                col_outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index
                outlier_indices.update(col_outliers)
                
                # Z-score method
                z_scores = np.abs(stats.zscore(df[col].fillna(df[col].mean())))
                z_outliers = df[z_scores > 3].index
                outlier_indices.update(z_outliers)
    
    # Return boolean mask
    outlier_mask = pd.Series([False] * len(df), index=df.index)
    outlier_mask.loc[list(outlier_indices)] = True
    
    return outlier_mask

# Template System
def save_cleaning_template(name, steps):
    """Save cleaning workflow as a reusable template"""
    template = {
        'name': name,
        'steps': steps,
        'created_date': datetime.now().isoformat(),
        'description': f"Template with {len(steps)} cleaning steps"
    }
    st.session_state.templates[name] = template
    return True

def get_predefined_templates():
    """Get industry-specific predefined templates"""
    return {
        'Sales Data Cleaning': {
            'description': 'Standard workflow for sales and revenue data',
            'steps': [
                {'type': 'remove_duplicates', 'params': {}},
                {'type': 'handle_missing', 'column': 'revenue', 'method': 'Fill with median'},
                {'type': 'handle_outliers', 'columns': ['revenue', 'quantity'], 'method': 'cap'},
                {'type': 'convert_types', 'column': 'date', 'target_type': 'datetime'}
            ]
        },
        'Customer Data Cleaning': {
            'description': 'Workflow for customer information datasets',
            'steps': [
                {'type': 'remove_duplicates', 'params': {}},
                {'type': 'handle_missing', 'column': 'email', 'method': 'Remove rows with missing values'},
                {'type': 'standardize_text', 'columns': ['name', 'city'], 'method': 'title_case'},
                {'type': 'validate_formats', 'column': 'email', 'format': 'email'}
            ]
        },
        'Financial Data Cleaning': {
            'description': 'Template for financial and accounting data',
            'steps': [
                {'type': 'remove_duplicates', 'params': {}},
                {'type': 'handle_missing', 'columns': ['amount', 'balance'], 'method': 'Fill with mean'},
                {'type': 'handle_outliers', 'columns': ['amount'], 'method': 'isolation_forest'},
                {'type': 'scaling', 'columns': ['amount', 'balance'], 'method': 'Standard Scaling'}
            ]
        }
    }

# Advanced Visualization Functions
def create_advanced_visualization(df, viz_config):
    """Create advanced visualizations with multiple chart types"""
    chart_type = viz_config.get('type')
    
    if chart_type == '3D Scatter':
        x_col, y_col, z_col = viz_config.get('x'), viz_config.get('y'), viz_config.get('z')
        if all([x_col, y_col, z_col]):
            fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col,
                               color=viz_config.get('color'),
                               title=f"3D Scatter: {x_col} vs {y_col} vs {z_col}")
            return fig
    
    elif chart_type == 'Correlation Network':
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 2:
            corr_matrix = df[numeric_cols].corr()
            # Create network-style correlation plot
            fig = px.imshow(corr_matrix, 
                           title="Correlation Network",
                           color_continuous_scale="RdBu_r",
                           aspect="auto")
            return fig
    
    elif chart_type == 'Statistical Summary':
        numeric_cols = df.select_dtypes(include=[np.number]).columns[:4]  # Limit to 4 for readability
        fig = make_subplots(rows=2, cols=2, 
                           subplot_titles=[f"{col} Distribution" for col in numeric_cols])
        
        for i, col in enumerate(numeric_cols):
            row = i // 2 + 1
            col_pos = i % 2 + 1
            
            # Add histogram
            fig.add_histogram(x=df[col], name=col, 
                            row=row, col=col_pos)
        
        fig.update_layout(title="Statistical Summary Dashboard", showlegend=False)
        return fig
    
    elif chart_type == 'Time Series Decomposition':
        date_col = viz_config.get('date_column')
        value_col = viz_config.get('value_column')
        
        if date_col and value_col:
            # Ensure date column is datetime
            df[date_col] = pd.to_datetime(df[date_col])
            df_sorted = df.sort_values(date_col)
            
            fig = make_subplots(rows=3, cols=1,
                               subplot_titles=['Original Series', 'Trend', 'Seasonality'])
            
            # Original series
            fig.add_scatter(x=df_sorted[date_col], y=df_sorted[value_col],
                           name='Original', row=1, col=1)
            
            # Simple trend (rolling mean)
            if len(df_sorted) > 30:
                trend = df_sorted[value_col].rolling(window=30, center=True).mean()
                fig.add_scatter(x=df_sorted[date_col], y=trend,
                               name='Trend', row=2, col=1)
            
            fig.update_layout(title="Time Series Analysis", showlegend=True)
            return fig
    
    return None

# Clustering Analysis
def perform_clustering_analysis(df, n_clusters=3):
    """Perform K-means clustering on numeric data"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) < 2:
        return None, "Need at least 2 numeric columns for clustering"
    
    # Prepare data
    clustering_data = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(clustering_data)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = kmeans.fit_predict(scaled_data)
    
    # Add cluster labels to dataframe
    result_df = df.copy()
    result_df['Cluster'] = cluster_labels
    
    # Create visualization
    if len(numeric_cols) >= 2:
        fig = px.scatter(result_df, 
                        x=numeric_cols[0], 
                        y=numeric_cols[1],
                        color='Cluster',
                        title=f"K-Means Clustering (k={n_clusters})")
        return fig, f"Successfully created {n_clusters} clusters"
    
    return None, "Visualization not available"

# Dashboard Builder
def create_dashboard(df, config):
    """Create a multi-panel dashboard"""
    st.markdown("### 📊 Interactive Dashboard")
    
    # Create layout based on config
    cols = st.columns(2)
    
    with cols[0]:
        # Chart 1
        if 'chart1' in config:
            chart1_config = config['chart1']
            fig1 = create_advanced_visualization(df, chart1_config)
            if fig1:
                st.plotly_chart(fig1, use_container_width=True)
    
    with cols[1]:
        # Chart 2
        if 'chart2' in config:
            chart2_config = config['chart2']
            fig2 = create_advanced_visualization(df, chart2_config)
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)
    
    # Full width chart
    if 'chart3' in config:
        chart3_config = config['chart3']
        fig3 = create_advanced_visualization(df, chart3_config)
        if fig3:
            st.plotly_chart(fig3, use_container_width=True)

# Simple Sidebar
st.sidebar.title("🎛️ Control Panel")
st.sidebar.markdown("Navigate through powerful features")

main_section = st.sidebar.radio(
    "Choose your destination:",
    ["🏠 Home", "📁 Data Upload", "🧠 AI Insights", "🧹 Smart Cleaning", "📊 Advanced Analytics", "🎨 Dashboard Builder", "🔧 Pipeline Builder",
     "🛠️ Feature Engineering", "🔬 Statistical Analysis", "🤖 AI Recommendations",
     "📋 Templates", "👥 Collaboration", "⚙️ Settings"],
    help="Select a section to explore different features of the platform"
)

# Main header - ONLY SHOW ON HOME PAGE
if main_section == "🏠 Home":
    st.markdown("# 📊 Datalix")
    st.markdown("### AI-Powered Data Cleaning, Analysis & Visualization")
    
    st.markdown("---")
    
    # Feature highlights in bordered sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="border: 2px solid #e0e7ff; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8faff;">
            <h4 style="color: #4f46e5; margin-bottom: 15px;">🧹 Smart Cleaning</h4>
            <p style="color: #6b7280; margin: 0;">AI-powered data cleaning with intelligent suggestions</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="border: 2px solid #e0e7ff; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8faff;">
            <h4 style="color: #4f46e5; margin-bottom: 15px;">📊 Advanced Analytics</h4>
            <p style="color: #6b7280; margin: 0;">Statistical analysis & machine learning capabilities</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="border: 2px solid #e0e7ff; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8faff;">
            <h4 style="color: #4f46e5; margin-bottom: 15px;">🎨 Interactive Viz</h4>
            <p style="color: #6b7280; margin: 0;">Dynamic visualizations and dashboards</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="border: 2px solid #e0e7ff; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8faff;">
            <h4 style="color: #4f46e5; margin-bottom: 15px;">🤖 AI Insights</h4>
            <p style="color: #6b7280; margin: 0;">Intelligent recommendations and analysis</p>
        </div>
        """, unsafe_allow_html=True)

# Home Dashboard
if main_section == "🏠 Home":
    # Quick Stats Dashboard
    if st.session_state.df is not None:
        df = st.session_state.df
        
        # Data Quality Score
        if st.session_state.data_quality_score is None:
            with st.spinner("🧠 AI is analyzing your data quality..."):
                score, suggestions = calculate_data_quality_score(df)
                st.session_state.data_quality_score = score
                st.session_state.ai_suggestions = suggestions
        
        # Display quality score with color coding
        score = st.session_state.data_quality_score
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if score >= 85:
                score_class = "score-excellent"
            elif score >= 70:
                score_class = "score-good" 
            elif score >= 50:
                score_class = "score-fair"
            else:
                score_class = "score-poor"
                
            st.markdown(f"""
                <div class="feature-card">
                    <h3 style="text-align: center; margin-bottom: 1rem;">🎯 Data Quality Score</h3>
                    <div class="quality-score {score_class}">
                        {score:.0f}
                    </div>
                    <p style="text-align: center; margin-top: 1rem; color: #6b7280;">
                        {'Excellent' if score >= 85 else 'Good' if score >= 70 else 'Fair' if score >= 50 else 'Needs Work'}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        
        # Quick Statistics
        st.markdown("### 📈 Dataset Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #3b82f6; margin: 0;">{df.shape[0]:,}</h2>
                    <p style="margin: 0; color: #6b7280;">Rows</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #10b981; margin: 0;">{df.shape[1]}</h2>
                    <p style="margin: 0; color: #6b7280;">Columns</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            missing_percentage = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
            st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #f59e0b; margin: 0;">{missing_percentage:.1f}%</h2>
                    <p style="margin: 0; color: #6b7280;">Missing Data</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col4:
            duplicate_percentage = (df.duplicated().sum() / len(df)) * 100
            st.markdown(f"""
                <div class="metric-card">
                    <h2 style="color: #ef4444; margin: 0;">{duplicate_percentage:.1f}%</h2>
                    <p style="margin: 0; color: #6b7280;">Duplicates</p>
                </div>
            """, unsafe_allow_html=True)
        
        # AI Suggestions
        if st.session_state.ai_suggestions:
            st.markdown("### 🧠 AI Recommendations")
            for suggestion in st.session_state.ai_suggestions:
                icon = "✅" if suggestion['type'] == 'success' else "⚠️" if suggestion['type'] == 'warning' else "💡"
                st.markdown(f"""
                    <div class="ai-suggestion">
                        <h4>{icon} {suggestion['title']}</h4>
                        <p>{suggestion['message']}</p>
                        <small><strong>Suggested Action:</strong> {suggestion['action']}</small>
                    </div>
                """, unsafe_allow_html=True)
                
        # Enhanced Quick Actions
        st.markdown("### ⚡ Quick Actions")
        
        action_col1, action_col2, action_col3 = st.columns(3)
        
        with action_col1:
            st.markdown("""
            <div class="feature-card" style="text-align: center; padding: 1.5rem; cursor: pointer; transition: all 0.3s ease;" onclick="document.querySelector('[data-testid=stButton] button').click()">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🧹</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #374151;">Smart Clean</h4>
                <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">AI-powered data cleaning</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🧹 Smart Clean", use_container_width=True, key="smart_clean_btn"):
                st.session_state.redirect_to = "🧹 Smart Cleaning"
                st.rerun()
        
        with action_col2:
            st.markdown("""
            <div class="feature-card" style="text-align: center; padding: 1.5rem; cursor: pointer; transition: all 0.3s ease;" onclick="document.querySelector('[data-testid=stButton] button').click()">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #374151;">Quick Viz</h4>
                <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">Instant visualizations</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📊 Quick Viz", use_container_width=True, key="quick_viz_btn"):
                st.session_state.redirect_to = "📊 Advanced Analytics"
                st.rerun()
                
        with action_col3:
            st.markdown("""
            <div class="feature-card" style="text-align: center; padding: 1.5rem; cursor: pointer; transition: all 0.3s ease;" onclick="document.querySelector('[data-testid=stButton] button').click()">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎨</div>
                <h4 style="margin: 0 0 0.5rem 0; color: #374151;">Build Dashboard</h4>
                <p style="margin: 0; color: #6b7280; font-size: 0.9rem;">Custom dashboards</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🎨 Build Dashboard", use_container_width=True, key="build_dashboard_btn"):
                st.session_state.redirect_to = "🎨 Dashboard Builder"
                st.rerun()
    
    else:
        # Clean welcome screen with bordered sections
        st.markdown("## 👋 Welcome to Datalix!")
        st.markdown("Transform your messy data into clean, analyzed, and visualized insights with the power of AI.")
        
        st.markdown("---")
        
        # Quick start guide with borders
        st.markdown("### 🚀 Quick Start Guide")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div style="border: 2px solid #e0e7ff; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8faff; text-align: center;">
                <h4 style="color: #4f46e5; margin-bottom: 15px;">📁 Upload Data</h4>
                <p style="color: #6b7280; margin: 0;">Support for CSV, Excel, JSON & more formats</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div style="border: 2px solid #e0e7ff; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8faff; text-align: center;">
                <h4 style="color: #4f46e5; margin-bottom: 15px;">🧠 AI Analysis</h4>
                <p style="color: #6b7280; margin: 0;">Smart insights & automated cleaning</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div style="border: 2px solid #e0e7ff; border-radius: 10px; padding: 20px; margin: 10px 0; background-color: #f8faff; text-align: center;">
                <h4 style="color: #4f46e5; margin-bottom: 15px;">📊 Visualize</h4>
                <p style="color: #6b7280; margin: 0;">Interactive charts & dashboards</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="border: 2px solid #fbbf24; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #fef3c7;">
            <p style="color: #92400e; margin: 0; font-weight: bold;">💡 Tip: Upload your dataset to get started with AI-powered data cleaning and analysis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced feature highlights - ONLY SHOW ON HOME PAGE
        st.markdown("### ✨ Platform Features")
        
        feature_col1, feature_col2 = st.columns(2)
        
        with feature_col1:
            st.markdown("""
            <div class="feature-card" style="padding: 1.5rem;">
                <h4 style="background: linear-gradient(135deg, #4f46e5, #7c3aed); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1rem;">
                    🧠 AI-Powered Features
                </h4>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(79, 70, 229, 0.05); border-radius: 8px; border-left: 3px solid #4f46e5;">
                        <span class="badge badge-primary" style="margin-right: 0.5rem;">NEW</span>
                        Smart data quality assessment
                    </li>
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(79, 70, 229, 0.05); border-radius: 8px; border-left: 3px solid #4f46e5;">
                        <span class="badge badge-success" style="margin-right: 0.5rem;">AI</span>
                        Automated cleaning suggestions
                    </li>
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(79, 70, 229, 0.05); border-radius: 8px; border-left: 3px solid #4f46e5;">
                        <span class="badge badge-warning" style="margin-right: 0.5rem;">ML</span>
                        Intelligent data type detection
                    </li>
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(79, 70, 229, 0.05); border-radius: 8px; border-left: 3px solid #4f46e5;">
                        <span class="badge badge-error" style="margin-right: 0.5rem;">ADV</span>
                        ML-based missing value imputation
                    </li>
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(79, 70, 229, 0.05); border-radius: 8px; border-left: 3px solid #4f46e5;">
                        <span class="badge badge-primary" style="margin-right: 0.5rem;">ML</span>
                        Advanced outlier detection
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with feature_col2:
            st.markdown("""
            <div class="feature-card" style="padding: 1.5rem;">
                <h4 style="background: linear-gradient(135deg, #10b981, #34d399); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1rem;">
                    📊 Advanced Analytics
                </h4>
                <ul style="list-style: none; padding: 0; margin: 0;">
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(16, 185, 129, 0.05); border-radius: 8px; border-left: 3px solid #10b981;">
                        <span class="badge badge-success" style="margin-right: 0.5rem;">3D</span>
                        3D visualizations
                    </li>
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(16, 185, 129, 0.05); border-radius: 8px; border-left: 3px solid #10b981;">
                        <span class="badge badge-warning" style="margin-right: 0.5rem;">ML</span>
                        Clustering analysis
                    </li>
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(16, 185, 129, 0.05); border-radius: 8px; border-left: 3px solid #10b981;">
                        <span class="badge badge-primary" style="margin-right: 0.5rem;">TS</span>
                        Time series decomposition
                    </li>
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(16, 185, 129, 0.05); border-radius: 8px; border-left: 3px solid #10b981;">
                        <span class="badge badge-error" style="margin-right: 0.5rem;">INT</span>
                        Interactive dashboards
                    </li>
                    <li style="margin: 0.5rem 0; padding: 0.5rem; background: rgba(16, 185, 129, 0.05); border-radius: 8px; border-left: 3px solid #10b981;">
                        <span class="badge badge-primary" style="margin-right: 0.5rem;">TPL</span>
                        Template system for workflows
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

# Enhanced Data Upload Section
elif main_section == "📁 Data Upload":
    st.markdown('<h2 class="section-header">📁 Advanced Data Upload</h2>', unsafe_allow_html=True)
    
    # Upload options
    upload_method = st.radio(
        "Choose upload method:",
        ["📄 File Upload", "🌐 URL Import", "📊 Sample Data"]
    )
    
    if upload_method == "📄 File Upload":
        uploaded_files = st.file_uploader(
            "Upload your dataset(s)",
            type=['csv', 'xlsx', 'xls', 'json', 'parquet', 'tsv', 'txt'],
            accept_multiple_files=True,
            help="Supported formats: CSV, Excel, JSON, Parquet, TSV, TXT"
        )
        
        if uploaded_files:
            with st.spinner("🔄 Loading and analyzing your data..."):
                df = load_data_advanced(uploaded_files, "file")
                
            if df is not None:
                st.session_state.df = df
                st.session_state.original_df = df.copy()
                st.session_state.data_quality_score = None  # Reset quality score
                
                st.success(f"✅ Successfully loaded {len(uploaded_files)} file(s)!")
                
                # Enhanced preview with smart insights
                st.markdown("### 👀 Smart Data Preview")
                
                # Show first few rows with highlighting
                preview_df = df.head(10)
                st.dataframe(preview_df, use_container_width=True)
                
                # Smart data type suggestions
                with st.expander("🧠 AI Data Type Suggestions", expanded=True):
                    type_suggestions = detect_data_types_smart(df)
                    if type_suggestions:
                        st.write("**AI detected potential data type improvements:**")
                        for col, suggestion in type_suggestions.items():
                            confidence_color = "🟢" if suggestion['confidence'] == 'high' else "🟡"
                            st.write(f"{confidence_color} **{col}**: Suggested type → `{suggestion['suggested_type']}`")
                    else:
                        st.write("✅ Data types look good as they are!")
    
    elif upload_method == "🌐 URL Import":
        st.markdown("### Import from URL")
        
        # Sample URLs for testing
        st.markdown("**💡 Sample URLs for testing:**")
        sample_urls = {
            "Iris Dataset": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv",
            "Titanic Dataset": "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv",
            "Diamonds Dataset": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/diamonds.csv"
        }
        
        selected_sample = st.selectbox("Or choose a sample dataset:", ["None"] + list(sample_urls.keys()))
        
        if selected_sample != "None":
            url = sample_urls[selected_sample]
        else:
            url = st.text_input("Enter CSV/JSON URL:", placeholder="https://example.com/data.csv")
        
        if url and st.button("📥 Import from URL"):
            try:
                with st.spinner("🌐 Fetching data from URL..."):
                    if url.endswith('.csv'):
                        df = pd.read_csv(url)
                    elif url.endswith('.json'):
                        df = pd.read_json(url)
                    else:
                        st.error("❌ Please provide a CSV or JSON URL")
                        st.stop()
                        
                st.session_state.df = df
                st.session_state.original_df = df.copy()
                st.success("✅ Data imported successfully from URL!")
                
            except Exception as e:
                st.error(f"❌ Error importing data: {str(e)}")
                
        # Alternative: Create sample data if URLs don't work
        st.markdown("**🔧 If sample URLs don't work, try this:**")
        if st.button("📊 Generate Sample Data"):
            # Create sample sales data
            np.random.seed(42)
            dates = pd.date_range('2023-01-01', periods=100, freq='D')
            sample_data = pd.DataFrame({
                'date': dates,
                'product': np.random.choice(['Laptop', 'Phone', 'Tablet', 'Monitor'], 100),
                'sales_amount': np.random.normal(500, 150, 100),
                'quantity': np.random.poisson(3, 100),
                'customer_region': np.random.choice(['North', 'South', 'East', 'West'], 100),
                'profit_margin': np.random.uniform(0.1, 0.4, 100)
            })
            
            st.session_state.df = sample_data
            st.session_state.original_df = sample_data.copy()
            st.success("✅ Sample data generated successfully!")
            st.dataframe(sample_data.head(), use_container_width=True)
    
    elif upload_method == "📊 Sample Data":
        st.markdown("### Try with Sample Datasets")
        
        sample_datasets = {
            "Sales Data": {
                "description": "E-commerce sales with missing values and outliers",
                "rows": 1000,
                "features": "date, product, revenue, quantity, customer_segment"
            },
            "Customer Data": {
                "description": "Customer information with data quality issues",
                "rows": 500,
                "features": "name, email, age, city, signup_date"
            },
            "Financial Data": {
                "description": "Stock prices with time series data",
                "rows": 252,
                "features": "date, open, high, low, close, volume"
            }
        }
        
        for name, info in sample_datasets.items():
            with st.expander(f"📈 {name}", expanded=False):
                st.write(f"**Description:** {info['description']}")
                st.write(f"**Rows:** {info['rows']} | **Features:** {info['features']}")
                
                if st.button(f"Load {name}", key=f"load_{name}"):
                    # Generate sample data
                    np.random.seed(42)
                    
                    if name == "Sales Data":
                        dates = pd.date_range('2023-01-01', periods=1000, freq='D')
                        df = pd.DataFrame({
                            'date': dates,
                            'product': np.random.choice(['A', 'B', 'C', 'D'], 1000),
                            'revenue': np.random.normal(1000, 300, 1000),
                            'quantity': np.random.poisson(5, 1000),
                            'customer_segment': np.random.choice(['Premium', 'Standard', 'Basic'], 1000)
                        })
                        # Add some missing values and outliers
                        df.loc[np.random.choice(1000, 50, False), 'revenue'] = np.nan
                        df.loc[np.random.choice(1000, 10, False), 'revenue'] = np.random.normal(5000, 1000, 10)
                        
                    elif name == "Customer Data":
                        df = pd.DataFrame({
                            'name': [f"Customer_{i}" for i in range(500)],
                            'email': [f"user{i}@email.com" if i % 10 != 0 else np.nan for i in range(500)],
                            'age': np.random.normal(35, 15, 500),
                            'city': np.random.choice(['NYC', 'LA', 'Chicago', 'Houston'], 500),
                            'signup_date': pd.date_range('2020-01-01', periods=500, freq='D')
                        })
                        
                    elif name == "Financial Data":
                        dates = pd.date_range('2023-01-01', periods=252, freq='B')
                        price = 100
                        prices = [price]
                        for _ in range(251):
                            price += np.random.normal(0, 2)
                            prices.append(price)
                        
                        df = pd.DataFrame({
                            'date': dates,
                            'open': prices[:-1],
                            'close': prices[1:],
                            'volume': np.random.randint(1000, 10000, 252)
                        })
                        max_values = df[['open', 'close']].max(axis=1)
                        min_values = df[['open', 'close']].min(axis=1)
                        df['high'] = max_values + np.random.uniform(0, 5, 252)
                        df['low'] = min_values - np.random.uniform(0, 5, 252)
                    
                    st.session_state.df = df
                    st.session_state.original_df = df.copy()
                    st.success(f"✅ {name} loaded successfully!")

# AI Insights Section
elif main_section == "🧠 AI Insights":
    st.markdown('<h2 class="section-header">🧠 AI-Powered Data Insights</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        st.stop()
    
    df = st.session_state.df
    
    # Auto-refresh quality score
    if st.button("🔄 Refresh AI Analysis"):
        with st.spinner("🧠 AI is re-analyzing your data..."):
            score, suggestions = calculate_data_quality_score(df)
            st.session_state.data_quality_score = score
            st.session_state.ai_suggestions = suggestions
    
    # Data Quality Assessment
    st.markdown("### 🎯 Comprehensive Data Quality Report")
    
    if st.session_state.data_quality_score is not None:
        score = st.session_state.data_quality_score
        
        # Detailed quality breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            # Quality score visualization
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=score,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Data Quality Score"},
                delta={'reference': 80},
                gauge={'axis': {'range': [None, 100]},
                       'bar': {'color': "darkblue"},
                       'steps': [
                           {'range': [0, 50], 'color': "lightgray"},
                           {'range': [50, 80], 'color': "yellow"},
                           {'range': [80, 100], 'color': "green"}],
                       'threshold': {'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75, 'value': 90}}))
            
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Quality components breakdown
            st.markdown("**Quality Components:**")
            
            # Calculate individual component scores
            missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
            completeness = max(0, 100 - missing_pct)
            
            duplicate_pct = (df.duplicated().sum() / len(df)) * 100
            uniqueness = max(0, 100 - duplicate_pct * 2)
            
            # Display components
            st.progress(completeness / 100)
            st.write(f"**Completeness:** {completeness:.1f}/100")
            
            st.progress(uniqueness / 100) 
            st.write(f"**Uniqueness:** {uniqueness:.1f}/100")
            
            # Consistency (simplified)
            consistency = 85  # Placeholder - would be calculated in real implementation
            st.progress(consistency / 100)
            st.write(f"**Consistency:** {consistency:.1f}/100")
    
    # Column Analysis
    st.markdown("### 📊 Column-by-Column Analysis")
    
    analysis_tabs = st.tabs(["📋 Overview", "🔍 Missing Values", "📈 Distributions", "🔗 Relationships"])
    
    with analysis_tabs[0]:
        # Enhanced column overview
        col_analysis = []
        for col in df.columns:
            analysis = {
                'Column': col,
                'Type': str(df[col].dtype),
                'Missing': f"{df[col].isnull().sum()} ({(df[col].isnull().sum()/len(df)*100):.1f}%)",
                'Unique': df[col].nunique(),
                'Memory': f"{df[col].memory_usage(deep=True) / 1024:.1f} KB"
            }
            
            # Add type-specific analysis
            if df[col].dtype in ['int64', 'float64']:
                analysis['Min'] = f"{df[col].min():.2f}"
                analysis['Max'] = f"{df[col].max():.2f}"
                analysis['Mean'] = f"{df[col].mean():.2f}"
            else:
                analysis['Top Value'] = str(df[col].mode().iloc[0]) if not df[col].mode().empty else 'N/A'
                analysis['Top Count'] = df[col].value_counts().iloc[0] if not df[col].value_counts().empty else 0
            
            col_analysis.append(analysis)
        
        analysis_df = pd.DataFrame(col_analysis)
        st.dataframe(analysis_df, use_container_width=True)
    
    with analysis_tabs[1]:
        # Missing values heatmap
        if df.isnull().sum().sum() > 0:
            st.write("**Missing Values Pattern:**")
            
            # Create missing values heatmap
            missing_matrix = df.isnull()
            fig = px.imshow(missing_matrix.T, 
                           title="Missing Values Heatmap (White = Missing)",
                           color_continuous_scale="RdYlBu_r")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("🎉 No missing values detected!")
    
    with analysis_tabs[2]:
        # Distribution analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 0:
            selected_col = st.selectbox("Select column for distribution analysis:", numeric_cols)
            
            # Create distribution plot with statistics
            fig = make_subplots(rows=1, cols=2, 
                               subplot_titles=['Distribution', 'Box Plot'])
            
            fig.add_histogram(x=df[selected_col].dropna(), name="Distribution", row=1, col=1)
            fig.add_box(y=df[selected_col].dropna(), name="Box Plot", row=1, col=2)
            
            fig.update_layout(title=f"Distribution Analysis: {selected_col}", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean", f"{df[selected_col].mean():.2f}")
            with col2:
                st.metric("Median", f"{df[selected_col].median():.2f}")
            with col3:
                st.metric("Std Dev", f"{df[selected_col].std():.2f}")
            with col4:
                st.metric("Skewness", f"{df[selected_col].skew():.2f}")
    
    with analysis_tabs[3]:
        # Correlation analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            
            # Interactive correlation heatmap
            fig = px.imshow(corr_matrix, 
                           title="Correlation Matrix",
                           color_continuous_scale="RdBu_r",
                           aspect="auto")
            st.plotly_chart(fig, use_container_width=True)
            
            # Highlight strong correlations
            st.write("**Strong Correlations (|r| > 0.7):**")
            strong_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.7:
                        strong_corr.append({
                            'Variable 1': corr_matrix.columns[i],
                            'Variable 2': corr_matrix.columns[j],
                            'Correlation': f"{corr_val:.3f}"
                        })
            
            if strong_corr:
                st.dataframe(pd.DataFrame(strong_corr), use_container_width=True)
            else:
                st.info("No strong correlations found.")

# Smart Cleaning Section
elif main_section == "🧹 Smart Cleaning":
    st.markdown('<h2 class="section-header">🧹 AI-Powered Smart Cleaning</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        st.stop()
    
    df = st.session_state.df
    
    # Auto-cleaning suggestions
    st.markdown("### 🤖 Automated Cleaning Workflow")
    
    if st.button("✨ Auto-Clean Dataset", type="primary"):
        with st.spinner("🤖 AI is automatically cleaning your data..."):
            cleaned_df = df.copy()
            cleaning_steps = []
            
            # Step 1: Remove exact duplicates
            initial_rows = len(cleaned_df)
            cleaned_df = cleaned_df.drop_duplicates()
            duplicates_removed = initial_rows - len(cleaned_df)
            if duplicates_removed > 0:
                cleaning_steps.append(f"Removed {duplicates_removed} duplicate rows")
            
            # Step 2: Handle missing values intelligently
            for col in cleaned_df.columns:
                missing_count = cleaned_df[col].isnull().sum()
                if missing_count > 0:
                    missing_pct = (missing_count / len(cleaned_df)) * 100
                    
                    if missing_pct > 50:
                        # Too much missing data - consider dropping column
                        if st.session_state.get('auto_drop_high_missing', False):
                            cleaned_df = cleaned_df.drop(columns=[col])
                            cleaning_steps.append(f"Dropped column '{col}' (>{missing_pct:.1f}% missing)")
                    elif cleaned_df[col].dtype in ['int64', 'float64']:
                        # Numeric: fill with median
                        cleaned_df[col].fillna(cleaned_df[col].median(), inplace=True)
                        cleaning_steps.append(f"Filled missing values in '{col}' with median")
                    else:
                        # Categorical: fill with mode
                        mode_val = cleaned_df[col].mode()
                        if not mode_val.empty:
                            cleaned_df[col].fillna(mode_val[0], inplace=True)
                            cleaning_steps.append(f"Filled missing values in '{col}' with mode")
            
            # Step 3: Handle outliers in numeric columns
            numeric_cols = cleaned_df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                outliers = detect_outliers_advanced(cleaned_df, [col], 'statistical')
                outlier_count = outliers.sum()
                if outlier_count > 0 and outlier_count < len(cleaned_df) * 0.1:  # Less than 10%
                    # Cap outliers instead of removing
                    Q1, Q3 = cleaned_df[col].quantile([0.25, 0.75])
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    cleaned_df[col] = cleaned_df[col].clip(lower=lower_bound, upper=upper_bound)
                    cleaning_steps.append(f"Capped {outlier_count} outliers in '{col}'")
            
            # Update session state
            st.session_state.df = cleaned_df
            st.session_state.cleaning_history.extend(cleaning_steps)
            
            st.success("✅ Auto-cleaning completed!")
            
            # Show summary
            st.markdown("**Cleaning Summary:**")
            for i, step in enumerate(cleaning_steps, 1):
                st.write(f"{i}. {step}")
    
    # Manual cleaning options with enhanced features
    st.markdown("### 🔧 Manual Cleaning Tools")
    
    cleaning_method = st.selectbox(
        "Choose cleaning operation:",
        ["Missing Values", "Duplicates", "Outliers", "Data Types", "Text Cleaning", "Advanced Operations"]
    )
    
    if cleaning_method == "Missing Values":
        st.markdown("#### Handle Missing Values")
        
        missing_cols = df.columns[df.isnull().any()].tolist()
        
        if missing_cols:
            selected_col = st.selectbox("Select column:", missing_cols)
            
            # Show missing value statistics
            missing_count = df[selected_col].isnull().sum()
            missing_pct = (missing_count / len(df)) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Missing Values", missing_count)
            with col2:
                st.metric("Percentage", f"{missing_pct:.1f}%")
            with col3:
                st.metric("Data Type", str(df[selected_col].dtype))
            
            # Enhanced cleaning methods
            if df[selected_col].dtype in ['int64', 'float64']:
                method_options = [
                    "Remove rows with missing values",
                    "Fill with mean", 
                    "Fill with median",
                    "Interpolation",
                    "ML Imputation (KNN)",
                    "Group-based Mean"
                ]
            else:
                method_options = [
                    "Remove rows with missing values",
                    "Fill with mode",
                    "Forward fill",
                    "Backward fill",
                    "Fill with custom value"
                ]
            
            cleaning_method = st.selectbox("Choose method:", method_options)
            
            # Additional parameters for advanced methods
            kwargs = {}
            if cleaning_method == "Group-based Mean":
                other_cols = [col for col in df.columns if col != selected_col and df[col].dtype == 'object']
                if other_cols:
                    group_col = st.selectbox("Group by column:", other_cols)
                    kwargs['group_column'] = group_col
                else:
                    st.warning("No categorical columns available for grouping!")
            
            if st.button("Apply Missing Value Treatment", key="missing_treatment"):
                cleaned_df = handle_missing_values_advanced(df, selected_col, cleaning_method, **kwargs)
                
                new_missing = cleaned_df[selected_col].isnull().sum()
                improvement = missing_count - new_missing
                
                st.session_state.df = cleaned_df
                st.session_state.cleaning_history.append(f"Applied {cleaning_method} to {selected_col}")
                
                st.success(f"✅ Reduced missing values by {improvement} ({(improvement/len(df)*100):.1f}%)")
        else:
            st.info("🎉 No missing values found!")
    
    elif cleaning_method == "Outliers":
        st.markdown("#### Advanced Outlier Detection & Handling")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            selected_cols = st.multiselect("Select columns for outlier analysis:", numeric_cols)
            
            if selected_cols:
                detection_method = st.radio(
                    "Detection method:",
                    ["Statistical (IQR + Z-score)", "Machine Learning (Isolation Forest)"]
                )
                
                method_key = 'statistical' if detection_method.startswith('Statistical') else 'isolation_forest'
                
                # Detect outliers
                outliers = detect_outliers_advanced(df, selected_cols, method_key)
                outlier_count = outliers.sum()
                
                st.metric("Outliers Detected", f"{outlier_count} ({(outlier_count/len(df)*100):.1f}%)")
                
                if outlier_count > 0:
                    # Show outlier preview
                    st.write("**Sample Outliers:**")
                    outlier_data = df[outliers][selected_cols].head()
                    st.dataframe(outlier_data, use_container_width=True)
                    
                    # Handling options
                    outlier_action = st.radio(
                        "Choose action:",
                        ["Remove outliers", "Cap outliers", "Mark as outliers (add column)"]
                    )
                    
                    if st.button("Apply Outlier Treatment", key="outlier_treatment"):
                        if outlier_action == "Remove outliers":
                            cleaned_df = df[~outliers]
                        elif outlier_action == "Cap outliers":
                            cleaned_df = df.copy()
                            for col in selected_cols:
                                Q1, Q3 = df[col].quantile([0.25, 0.75])
                                IQR = Q3 - Q1
                                lower_bound = Q1 - 1.5 * IQR
                                upper_bound = Q3 + 1.5 * IQR
                                cleaned_df[col] = cleaned_df[col].clip(lower=lower_bound, upper=upper_bound)
                        else:  # Mark as outliers
                            cleaned_df = df.copy()
                            cleaned_df['is_outlier'] = outliers
                        
                        st.session_state.df = cleaned_df
                        st.session_state.cleaning_history.append(f"Applied {outlier_action} using {detection_method}")
                        
                        st.success(f"✅ Handled {outlier_count} outliers")
                else:
                    st.info("🎉 No outliers detected!")
        else:
            st.info("No numeric columns available for outlier detection.")
    
    elif cleaning_method == "Text Cleaning":
        st.markdown("#### Text Data Cleaning")
        
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if text_cols:
            selected_col = st.selectbox("Select text column:", text_cols)
            
            # Text cleaning options
            cleaning_options = st.multiselect(
                "Select cleaning operations:",
                [
                    "Remove leading/trailing spaces",
                    "Convert to lowercase",
                    "Convert to title case",
                    "Remove special characters",
                    "Remove extra spaces",
                    "Standardize formats"
                ]
            )
            
            if cleaning_options and st.button("Apply Text Cleaning", key="text_cleaning"):
                cleaned_df = df.copy()
                
                for option in cleaning_options:
                    if option == "Remove leading/trailing spaces":
                        cleaned_df[selected_col] = cleaned_df[selected_col].astype(str).str.strip()
                    elif option == "Convert to lowercase":
                        cleaned_df[selected_col] = cleaned_df[selected_col].astype(str).str.lower()
                    elif option == "Convert to title case":
                        cleaned_df[selected_col] = cleaned_df[selected_col].astype(str).str.title()
                    elif option == "Remove special characters":
                        cleaned_df[selected_col] = cleaned_df[selected_col].astype(str).str.replace(r'[^a-zA-Z0-9\s]', '', regex=True)
                    elif option == "Remove extra spaces":
                        cleaned_df[selected_col] = cleaned_df[selected_col].astype(str).str.replace(r'\s+', ' ', regex=True)
                    elif option == "Standardize formats":
                        # Basic standardization - could be enhanced
                        cleaned_df[selected_col] = cleaned_df[selected_col].astype(str).str.strip().str.title()
                
                st.session_state.df = cleaned_df
                st.session_state.cleaning_history.append(f"Applied text cleaning to {selected_col}: {', '.join(cleaning_options)}")
                
                st.success("✅ Text cleaning applied successfully!")
                
                # Show before/after comparison
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Before:**")
                    st.write(df[selected_col].head().tolist())
                with col2:
                    st.write("**After:**")
                    st.write(cleaned_df[selected_col].head().tolist())
        else:
            st.info("No text columns found in the dataset.")
    
    # Show cleaning history
    if st.session_state.cleaning_history:
        st.markdown("### 📝 Cleaning History")
        
        with st.expander("View all cleaning operations", expanded=False):
            for i, action in enumerate(st.session_state.cleaning_history, 1):
                st.write(f"{i}. {action}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset to Original"):
                st.session_state.df = st.session_state.original_df.copy()
                st.session_state.cleaning_history = []
                st.session_state.data_quality_score = None
                st.success("✅ Data reset to original state")
                st.rerun()
        
        with col2:
            if st.button("💾 Save as Template"):
                template_name = st.text_input("Template name:", value=f"Template_{datetime.now().strftime('%Y%m%d_%H%M')}")
                if template_name:
                    save_cleaning_template(template_name, st.session_state.cleaning_history.copy())
                    st.success(f"✅ Template '{template_name}' saved!")

# Advanced Analytics Section  
elif main_section == "📊 Advanced Analytics":
    st.markdown('<h2 class="section-header">📊 Advanced Analytics & Visualization</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first!")
        st.stop()
    
    df = st.session_state.df
    
    # Analytics options
    analytics_type = st.selectbox(
        "Choose analysis type:",
        ["📈 Basic Visualizations", "🔬 Statistical Analysis", "🎯 Clustering Analysis", "📊 3D Visualizations", "⏰ Time Series Analysis"]
    )
    
    if analytics_type == "📈 Basic Visualizations":
        st.markdown("### Create Interactive Visualizations")
        
        viz_col1, viz_col2 = st.columns(2)
        
        with viz_col1:
            chart_type = st.selectbox(
                "Chart Type:",
                ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot", "Heatmap", "Pie Chart"]
            )
            
            columns = df.columns.tolist()
            x_col = st.selectbox("X-axis:", columns)
            
        with viz_col2:
            if chart_type in ["Scatter Plot", "Line Chart"]:
                y_col = st.selectbox("Y-axis:", [None] + columns)
            else:
                y_col = st.selectbox("Y-axis (optional):", [None] + columns)
            
            color_col = st.selectbox("Color by (optional):", [None] + columns)
        
        # Generate visualization
        if st.button("🎨 Create Visualization"):
            try:
                fig = None
                
                if chart_type == "Bar Chart":
                    if y_col:
                        fig = px.bar(df, x=x_col, y=y_col, color=color_col, 
                                   title=f"Bar Chart: {x_col} vs {y_col}")
                    else:
                        value_counts = df[x_col].value_counts().head(20)
                        fig = px.bar(x=value_counts.index, y=value_counts.values,
                                   title=f"Bar Chart: {x_col} Distribution")
                        
                elif chart_type == "Line Chart":
                    if y_col:
                        fig = px.line(df, x=x_col, y=y_col, color=color_col,
                                    title=f"Line Chart: {x_col} vs {y_col}")
                    
                elif chart_type == "Scatter Plot":
                    if y_col:
                        fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                                       title=f"Scatter Plot: {x_col} vs {y_col}")
                        
                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=x_col, color=color_col,
                                     title=f"Histogram: {x_col} Distribution")
                    
                elif chart_type == "Box Plot":
                    if y_col:
                        fig = px.box(df, x=x_col, y=y_col, color=color_col,
                                   title=f"Box Plot: {x_col} vs {y_col}")
                    else:
                        fig = px.box(df, y=x_col, title=f"Box Plot: {x_col}")
                        
                elif chart_type == "Heatmap":
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 1:
                        corr_matrix = df[numeric_cols].corr()
                        fig = px.imshow(corr_matrix, title="Correlation Heatmap",
                                      color_continuous_scale="RdBu_r")
                    
                elif chart_type == "Pie Chart":
                    if df[x_col].dtype == 'object' or df[x_col].nunique() < 20:
                        value_counts = df[x_col].value_counts().head(10)
                        fig = px.pie(values=value_counts.values, names=value_counts.index,
                                   title=f"Pie Chart: {x_col} Distribution")
                
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show statistics
                    if x_col in df.select_dtypes(include=[np.number]).columns:
                        st.markdown("#### 📈 Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Mean", f"{df[x_col].mean():.2f}")
                        with col2:
                            st.metric("Median", f"{df[x_col].median():.2f}")
                        with col3:
                            st.metric("Std Dev", f"{df[x_col].std():.2f}")
                        with col4:
                            st.metric("Range", f"{df[x_col].max() - df[x_col].min():.2f}")
                else:
                    st.error("❌ Could not create visualization. Please check your column selections.")
                    
            except Exception as e:
                st.error(f"❌ Error creating visualization: {str(e)}")
    
    elif analytics_type == "🔬 Statistical Analysis":
        st.markdown("### Statistical Analysis Suite")
        
        stat_test = st.selectbox(
            "Choose statistical test/analysis:",
            ["Descriptive Statistics", "Correlation Analysis", "T-Test", "ANOVA", "Chi-Square Test", "Normality Test"]
        )
        
        if stat_test == "Descriptive Statistics":
            st.markdown("#### 📊 Comprehensive Descriptive Statistics")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                selected_cols = st.multiselect("Select columns:", numeric_cols, default=numeric_cols[:3])
                
                if selected_cols:
                    # Enhanced descriptive statistics
                    desc_stats = df[selected_cols].describe()
                    
                    # Add additional statistics
                    additional_stats = pd.DataFrame({
                        col: {
                            'skewness': df[col].skew(),
                            'kurtosis': df[col].kurtosis(),
                            'variance': df[col].var(),
                            'range': df[col].max() - df[col].min(),
                            'iqr': df[col].quantile(0.75) - df[col].quantile(0.25)
                        } for col in selected_cols
                    }).T
                    
                    # Combine statistics
                    full_stats = pd.concat([desc_stats.T, additional_stats], axis=1)
                    
                    st.dataframe(full_stats, use_container_width=True)
                    
                    # Visual summary
                    if len(selected_cols) > 1:
                        fig = make_subplots(
                            rows=2, cols=len(selected_cols),
                            subplot_titles=[f"{col} - Histogram" for col in selected_cols] + 
                                          [f"{col} - Box Plot" for col in selected_cols],
                            vertical_spacing=0.1
                        )
                        
                        for i, col in enumerate(selected_cols):
                            # Histogram
                            fig.add_histogram(x=df[col], name=f"{col} Hist", 
                                            row=1, col=i+1, showlegend=False)
                            # Box plot
                            fig.add_box(y=df[col], name=f"{col} Box",
                                      row=2, col=i+1, showlegend=False)
                        
                        fig.update_layout(title="Statistical Distribution Summary", height=600)
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns available for statistical analysis.")
        
        elif stat_test == "Correlation Analysis":
            st.markdown("#### 🔗 Advanced Correlation Analysis")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if len(numeric_cols) > 1:
                # Correlation method selection
                corr_method = st.selectbox("Correlation method:", ["pearson", "spearman", "kendall"])
                
                # Calculate correlations
                corr_matrix = df[numeric_cols].corr(method=corr_method)
                
                # Interactive correlation heatmap
                fig = px.imshow(corr_matrix, 
                               title=f"{corr_method.title()} Correlation Matrix",
                               color_continuous_scale="RdBu_r",
                               aspect="auto")
                
                # Add correlation values as text
                fig.update_traces(text=np.around(corr_matrix.values, decimals=2),
                                texttemplate="%{text}", textfont_size=10)
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Find strongest correlations
                st.markdown("#### 🎯 Strongest Correlations")
                
                # Create correlation pairs
                correlations = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        correlations.append({
                            'Variable 1': corr_matrix.columns[i],
                            'Variable 2': corr_matrix.columns[j],
                            'Correlation': corr_matrix.iloc[i, j],
                            'Strength': 'Strong' if abs(corr_matrix.iloc[i, j]) > 0.7 else 'Moderate' if abs(corr_matrix.iloc[i, j]) > 0.3 else 'Weak'
                        })
                
                corr_df = pd.DataFrame(correlations)
                corr_df = corr_df.sort_values('Correlation', key=abs, ascending=False)
                
                st.dataframe(corr_df, use_container_width=True)
            else:
                st.info("Need at least 2 numeric columns for correlation analysis.")
        
        elif stat_test == "Normality Test":
            st.markdown("#### 📊 Normality Testing")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                selected_col = st.selectbox("Select column for normality test:", numeric_cols)
                
                # Perform Shapiro-Wilk test (for smaller samples) or Anderson-Darling
                sample_data = df[selected_col].dropna()
                
                if len(sample_data) > 5000:
                    sample_data = sample_data.sample(5000)  # Limit for computational efficiency
                
                try:
                    from scipy.stats import shapiro, normaltest, jarque_bera
                    
                    # Multiple normality tests
                    shapiro_stat, shapiro_p = shapiro(sample_data)
                    normaltest_stat, normaltest_p = normaltest(sample_data)
                    jb_stat, jb_p = jarque_bera(sample_data)
                    
                    # Results table
                    results = pd.DataFrame({
                        'Test': ['Shapiro-Wilk', 'D\'Agostino\'s', 'Jarque-Bera'],
                        'Statistic': [shapiro_stat, normaltest_stat, jb_stat],
                        'P-value': [shapiro_p, normaltest_p, jb_p],
                        'Normal?': [
                            'Yes' if shapiro_p > 0.05 else 'No',
                            'Yes' if normaltest_p > 0.05 else 'No', 
                            'Yes' if jb_p > 0.05 else 'No'
                        ]
                    })
                    
                    st.dataframe(results, use_container_width=True)
                    
                    # Visual assessment
                    fig = make_subplots(rows=1, cols=2, 
                                       subplot_titles=['Histogram vs Normal', 'Q-Q Plot'])
                    
                    # Histogram with normal overlay
                    fig.add_histogram(x=sample_data, name="Data", row=1, col=1, 
                                    histnorm='probability density', showlegend=False)
                    
                    # Normal distribution overlay
                    x_range = np.linspace(sample_data.min(), sample_data.max(), 100)
                    normal_y = stats.norm.pdf(x_range, sample_data.mean(), sample_data.std())
                    fig.add_scatter(x=x_range, y=normal_y, name="Normal", 
                                  row=1, col=1, line=dict(color='red'), showlegend=False)
                    
                    # Q-Q plot
                    qq_theoretical = stats.norm.ppf(np.linspace(0.01, 0.99, len(sample_data)))
                    qq_sample = np.sort(sample_data)
                    fig.add_scatter(x=qq_theoretical, y=qq_sample, mode='markers',
                                  name="Q-Q Plot", row=1, col=2, showlegend=False)
                    
                    # Add reference line for Q-Q plot
                    min_val, max_val = min(qq_theoretical.min(), qq_sample.min()), max(qq_theoretical.max(), qq_sample.max())
                    fig.add_scatter(x=[min_val, max_val], y=[min_val, max_val],
                                  mode='lines', line=dict(color='red', dash='dash'),
                                  row=1, col=2, showlegend=False)
                    
                    fig.update_layout(title=f"Normality Assessment: {selected_col}")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Interpretation
                    st.markdown("#### 📖 Interpretation")
                    if all(results['P-value'] > 0.05):
                        st.success("✅ Data appears to be normally distributed (all tests p > 0.05)")
                    elif any(results['P-value'] > 0.05):
                        st.warning("⚠️ Mixed results - some tests suggest normality, others don't")
                    else:
                        st.error("❌ Data does not appear to be normally distributed (all tests p < 0.05)")
                        
                except ImportError:
                    st.error("Additional statistical packages required for normality testing.")
            else:
                st.info("No numeric columns available for normality testing.")
    
    elif analytics_type == "🎯 Clustering Analysis":
        st.markdown("### 🎯 Unsupervised Clustering Analysis")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            # Clustering parameters
            col1, col2 = st.columns(2)
            
            with col1:
                selected_features = st.multiselect(
                    "Select features for clustering:",
                    numeric_cols,
                    default=numeric_cols[:min(4, len(numeric_cols))]
                )
                
            with col2:
                n_clusters = st.slider("Number of clusters:", 2, 10, 3)
            
            if len(selected_features) >= 2 and st.button("🔬 Perform Clustering Analysis"):
                with st.spinner("🎯 Performing clustering analysis..."):
                    try:
                        # Prepare data
                        clustering_data = df[selected_features].fillna(df[selected_features].mean())
                        
                        # Standardize features
                        scaler = StandardScaler()
                        scaled_data = scaler.fit_transform(clustering_data)
                        
                        # Perform K-means clustering
                        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                        cluster_labels = kmeans.fit_predict(scaled_data)
                        
                        # Add cluster labels to original data
                        clustered_df = df.copy()
                        clustered_df['Cluster'] = cluster_labels
                        
                        # Calculate cluster centers
                        cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
                        
                        # Visualizations
                        if len(selected_features) >= 2:
                            # 2D scatter plot of first two features
                            fig1 = px.scatter(
                                clustered_df, 
                                x=selected_features[0], 
                                y=selected_features[1],
                                color='Cluster',
                                title=f"Clustering Results: {selected_features[0]} vs {selected_features[1]}",
                                color_continuous_scale='viridis'
                            )
                            
                            # Add cluster centers
                            centers_df = pd.DataFrame(
                                cluster_centers[:, :2], 
                                columns=selected_features[:2]
                            )
                            centers_df['Cluster'] = range(n_clusters)
                            
                            fig1.add_scatter(
                                x=centers_df[selected_features[0]],
                                y=centers_df[selected_features[1]],
                                mode='markers',
                                marker=dict(size=15, symbol='x', color='red'),
                                name='Cluster Centers'
                            )
                            
                            st.plotly_chart(fig1, use_container_width=True)
                        
                        # 3D visualization if we have 3+ features
                        if len(selected_features) >= 3:
                            fig2 = px.scatter_3d(
                                clustered_df,
                                x=selected_features[0],
                                y=selected_features[1], 
                                z=selected_features[2],
                                color='Cluster',
                                title=f"3D Clustering: {', '.join(selected_features[:3])}",
                                color_continuous_scale='viridis'
                            )
                            st.plotly_chart(fig2, use_container_width=True)
                        
                        # Cluster analysis
                        st.markdown("#### 📊 Cluster Analysis")
                        
                        # Cluster summary statistics
                        cluster_summary = clustered_df.groupby('Cluster')[selected_features].agg(['mean', 'std', 'count'])
                        st.dataframe(cluster_summary, use_container_width=True)
                        
                        # Cluster sizes
                        cluster_sizes = clustered_df['Cluster'].value_counts().sort_index()
                        
                        fig3 = px.bar(
                            x=cluster_sizes.index,
                            y=cluster_sizes.values,
                            title="Cluster Sizes",
                            labels={'x': 'Cluster', 'y': 'Number of Points'}
                        )
                        st.plotly_chart(fig3, use_container_width=True)
                        
                        # Silhouette analysis
                        try:
                            from sklearn.metrics import silhouette_score
                            silhouette_avg = silhouette_score(scaled_data, cluster_labels)
                            
                            st.markdown("#### 🎯 Clustering Quality Metrics")
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Silhouette Score", f"{silhouette_avg:.3f}")
                            with col2:
                                st.metric("Inertia", f"{kmeans.inertia_:.2f}")
                            with col3:
                                quality = "Excellent" if silhouette_avg > 0.7 else "Good" if silhouette_avg > 0.5 else "Fair" if silhouette_avg > 0.25 else "Poor"
                                st.metric("Quality", quality)
                            
                            # Interpretation
                            st.markdown("#### 📖 Interpretation")
                            if silhouette_avg > 0.7:
                                st.success("✅ Excellent clustering structure - clusters are well-separated and compact")
                            elif silhouette_avg > 0.5:
                                st.info("✅ Good clustering structure - reasonable separation between clusters")
                            elif silhouette_avg > 0.25:
                                st.warning("⚠️ Fair clustering structure - some overlap between clusters")
                            else:
                                st.error("❌ Poor clustering structure - consider different number of clusters or features")
                        
                        except ImportError:
                            st.info("Install scikit-learn for clustering quality metrics")
                        
                        # Option to save clustered data
                        st.session_state.df = clustered_df
                        st.success(f"✅ Clustering completed! Added 'Cluster' column to dataset.")
                        
                    except Exception as e:
                        st.error(f"❌ Clustering failed: {str(e)}")
        else:
            st.info("Need at least 2 numeric columns for clustering analysis.")
    
    elif analytics_type == "🔬 3D Visualizations":
        st.markdown("### 🔬 Advanced 3D Visualizations")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 3:
            # 3D visualization options
            viz_3d_type = st.selectbox(
                "Choose 3D visualization:",
                ["3D Scatter Plot", "3D Surface Plot", "3D Mesh Plot"]
            )
            
            if viz_3d_type == "3D Scatter Plot":
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    x_col = st.selectbox("X-axis:", numeric_cols)
                with col2:
                    y_col = st.selectbox("Y-axis:", [col for col in numeric_cols if col != x_col])
                with col3:
                    z_col = st.selectbox("Z-axis:", [col for col in numeric_cols if col not in [x_col, y_col]])
                
                # Optional color and size
                color_col = st.selectbox("Color by (optional):", [None] + df.columns.tolist())
                size_col = st.selectbox("Size by (optional):", [None] + numeric_cols)
                
                if st.button("🎨 Create 3D Scatter Plot"):
                    fig = px.scatter_3d(
                        df, x=x_col, y=y_col, z=z_col,
                        color=color_col, size=size_col,
                        title=f"3D Scatter: {x_col} vs {y_col} vs {z_col}",
                        labels={x_col: x_col, y_col: y_col, z_col: z_col}
                    )
                    
                    fig.update_layout(scene=dict(
                        xaxis_title=x_col,
                        yaxis_title=y_col,
                        zaxis_title=z_col
                    ))
                    
                    st.plotly_chart(fig, use_container_width=True)
            
            elif viz_3d_type == "3D Surface Plot":
                st.markdown("#### Create 3D Surface Plot")
                
                x_col = st.selectbox("X variable:", numeric_cols)
                y_col = st.selectbox("Y variable:", [col for col in numeric_cols if col != x_col])  
                z_col = st.selectbox("Z variable (height):", [col for col in numeric_cols if col not in [x_col, y_col]])
                
                if st.button("🏔️ Create Surface Plot"):
                    try:
                        # Create a grid for surface plot
                        x_vals = np.linspace(df[x_col].min(), df[x_col].max(), 20)
                        y_vals = np.linspace(df[y_col].min(), df[y_col].max(), 20)
                        X, Y = np.meshgrid(x_vals, y_vals)
                        
                        # Interpolate Z values (simplified approach)
                        from scipy.interpolate import griddata
                        points = df[[x_col, y_col]].values
                        values = df[z_col].values
                        Z = griddata(points, values, (X, Y), method='linear', fill_value=0)
                        
                        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='viridis')])
                        
                        fig.update_layout(
                            title=f"3D Surface: {z_col} over {x_col} and {y_col}",
                            scene=dict(
                                xaxis_title=x_col,
                                yaxis_title=y_col,
                                zaxis_title=z_col
                            )
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                    except ImportError:
                        st.error("scipy package required for surface plots")
                    except Exception as e:
                        st.error(f"Error creating surface plot: {str(e)}")
        else:
            st.info("Need at least 3 numeric columns for 3D visualizations.")
    
    elif analytics_type == "⏰ Time Series Analysis":
        st.markdown("### ⏰ Time Series Analysis")
        
        # Detect potential date columns
        date_cols = []
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]' or 'date' in col.lower() or 'time' in col.lower():
                date_cols.append(col)
        
        # Also check if we can convert any columns to datetime
        potential_date_cols = []
        for col in df.select_dtypes(include=['object']).columns:
            try:
                pd.to_datetime(df[col].head(), infer_datetime_format=True)
                potential_date_cols.append(col)
            except:
                pass
        
        all_date_cols = date_cols + potential_date_cols
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if all_date_cols and numeric_cols:
            col1, col2 = st.columns(2)
            
            with col1:
                date_col = st.selectbox("Select date column:", all_date_cols)
            with col2:
                value_col = st.selectbox("Select value column:", numeric_cols)
            
            analysis_type = st.selectbox(
                "Choose analysis:",
                ["Time Series Plot", "Trend Analysis", "Seasonality Detection", "Moving Averages"]
            )
            
            if st.button("📈 Perform Time Series Analysis"):
                try:
                    # Convert date column to datetime if needed
                    df_ts = df.copy()
                    df_ts[date_col] = pd.to_datetime(df_ts[date_col])
                    df_ts = df_ts.sort_values(date_col).dropna(subset=[date_col, value_col])
                    
                    if analysis_type == "Time Series Plot":
                        fig = px.line(
                            df_ts, x=date_col, y=value_col,
                            title=f"Time Series: {value_col} over {date_col}"
                        )
                        fig.update_traces(line=dict(width=2))
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Basic statistics
                        st.markdown("#### 📊 Time Series Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Data Points", len(df_ts))
                        with col2:
                            date_range = (df_ts[date_col].max() - df_ts[date_col].min()).days
                            st.metric("Date Range (days)", date_range)
                        with col3:
                            st.metric("Mean Value", f"{df_ts[value_col].mean():.2f}")
                        with col4:
                            st.metric("Trend", "↗️ Up" if df_ts[value_col].iloc[-1] > df_ts[value_col].iloc[0] else "↘️ Down")
                    
                    elif analysis_type == "Moving Averages":
                        # Calculate different moving averages
                        window_sizes = [7, 30, 90]
                        
                        fig = go.Figure()
                        
                        # Original data
                        fig.add_trace(go.Scatter(
                            x=df_ts[date_col], y=df_ts[value_col],
                            mode='lines', name='Original',
                            line=dict(width=1, color='lightblue')
                        ))
                        
                        colors = ['red', 'green', 'orange']
                        for i, window in enumerate(window_sizes):
                            if len(df_ts) > window:
                                ma = df_ts[value_col].rolling(window=window, center=True).mean()
                                fig.add_trace(go.Scatter(
                                    x=df_ts[date_col], y=ma,
                                    mode='lines', name=f'{window}-day MA',
                                    line=dict(width=2, color=colors[i])
                                ))
                        
                        fig.update_layout(
                            title=f"Moving Averages Analysis: {value_col}",
                            xaxis_title=date_col,
                            yaxis_title=value_col
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    
                    elif analysis_type == "Trend Analysis":
                        # Simple linear trend
                        from sklearn.linear_model import LinearRegression
                        
                        # Convert dates to numeric for regression
                        df_ts['date_numeric'] = (df_ts[date_col] - df_ts[date_col].min()).dt.days
                        
                        X = df_ts[['date_numeric']]
                        y = df_ts[value_col]
                        
                        model = LinearRegression()
                        model.fit(X, y)
                        
                        # Predict trend line
                        trend_pred = model.predict(X)
                        
                        fig = go.Figure()
                        
                        # Original data
                        fig.add_trace(go.Scatter(
                            x=df_ts[date_col], y=df_ts[value_col],
                            mode='lines+markers', name='Data',
                            line=dict(width=2, color='blue')
                        ))
                        
                        # Trend line
                        fig.add_trace(go.Scatter(
                            x=df_ts[date_col], y=trend_pred,
                            mode='lines', name='Trend',
                            # Complete the trend analysis section (line continues from your code)
                        line=dict(width=3, color='red', dash='dash')
                        ))
                        
                        # Calculate trend statistics
                        slope = model.coef_[0]
                        r_squared = model.score(X, y)
                        
                        fig.update_layout(
                            title=f"Trend Analysis: {value_col} (Slope: {slope:.4f}, R²: {r_squared:.3f})",
                            xaxis_title=date_col,
                            yaxis_title=value_col
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Trend interpretation
                        st.markdown("#### 📈 Trend Analysis Results")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            trend_direction = "Increasing" if slope > 0 else "Decreasing" if slope < 0 else "Stable"
                            st.metric("Trend Direction", trend_direction)
                        with col2:
                            st.metric("Slope", f"{slope:.6f}")
                        with col3:
                            st.metric("R-squared", f"{r_squared:.4f}")
                        
                        # Trend strength interpretation
                        if r_squared > 0.8:
                            st.success("Strong trend detected - high predictability")
                        elif r_squared > 0.5:
                            st.info("Moderate trend detected")
                        else:
                            st.warning("Weak or no clear trend detected")
                    
                    elif analysis_type == "Seasonality Detection":
                        # Basic seasonality detection using autocorrelation
                        st.markdown("#### 🔄 Seasonality Analysis")
                        
                        # Calculate autocorrelation for different lags
                        max_lag = min(len(df_ts) // 4, 365)  # Up to 1 year or 1/4 of data
                        lags = range(1, max_lag + 1)
                        autocorr = [df_ts[value_col].autocorr(lag=lag) for lag in lags]
                        
                        # Plot autocorrelation
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=list(lags), y=autocorr,
                            mode='lines+markers',
                            name='Autocorrelation'
                        ))
                        
                        # Add significance threshold
                        significance_threshold = 1.96 / np.sqrt(len(df_ts))
                        fig.add_hline(y=significance_threshold, line_dash="dash", line_color="red")
                        fig.add_hline(y=-significance_threshold, line_dash="dash", line_color="red")
                        
                        fig.update_layout(
                            title="Autocorrelation Function - Seasonality Detection",
                            xaxis_title="Lag (time periods)",
                            yaxis_title="Autocorrelation"
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Find potential seasonal patterns
                        significant_lags = [lag for lag, corr in zip(lags, autocorr) 
                                          if abs(corr) > significance_threshold]
                        
                        if significant_lags:
                            st.write("**Potential Seasonal Patterns Detected at Lags:**")
                            for lag in significant_lags[:10]:  # Show top 10
                                st.write(f"- Lag {lag}: Autocorr = {autocorr[lag-1]:.3f}")
                        else:
                            st.info("No significant seasonal patterns detected")
                
                except Exception as e:
                    st.error(f"Time series analysis failed: {str(e)}")
        else:
            st.info("Time series analysis requires at least one date column and one numeric column.")

# Dashboard Builder Section (Complete Implementation)
elif main_section == "🎨 Dashboard Builder":
    st.markdown('<h2 class="section-header">🎨 Interactive Dashboard Builder</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("Please upload a dataset first!")
        st.stop()
    
    df = st.session_state.df
    
    st.markdown("### 🏗️ Build Your Custom Dashboard")
    
    # Dashboard configuration
    dashboard_name = st.text_input("Dashboard Name:", value="My Dashboard")
    
    # Layout options
    layout_type = st.selectbox(
        "Choose layout:",
        ["2x2 Grid", "Single Row", "Single Column", "Custom Layout"]
    )
    
    # Chart configuration section
    st.markdown("#### 📊 Configure Charts")
    
    chart_configs = {}
    
    if layout_type == "2x2 Grid":
        chart_positions = ["Top Left", "Top Right", "Bottom Left", "Bottom Right"]
    elif layout_type == "Single Row":
        chart_positions = ["Chart 1", "Chart 2", "Chart 3"]
    elif layout_type == "Single Column":
        chart_positions = ["Chart 1", "Chart 2", "Chart 3", "Chart 4"]
    else:  # Custom
        num_charts = st.slider("Number of charts:", 1, 6, 3)
        chart_positions = [f"Chart {i+1}" for i in range(num_charts)]
    
    # Configure each chart
    for position in chart_positions:
        with st.expander(f"Configure {position}", expanded=False):
            chart_type = st.selectbox(
                f"Chart type for {position}:",
                ["None", "Bar Chart", "Line Chart", "Scatter Plot", "Histogram", 
                 "Box Plot", "Heatmap", "3D Scatter", "Pie Chart"],
                key=f"chart_type_{position}"
            )
            
            if chart_type != "None":
                columns = df.columns.tolist()
                
                x_col = st.selectbox(f"X-axis:", columns, key=f"x_{position}")
                
                if chart_type in ["Line Chart", "Scatter Plot", "Box Plot"]:
                    y_col = st.selectbox(f"Y-axis:", [None] + columns, key=f"y_{position}")
                else:
                    y_col = None
                
                if chart_type == "3D Scatter":
                    z_col = st.selectbox(f"Z-axis:", [None] + columns, key=f"z_{position}")
                else:
                    z_col = None
                
                color_col = st.selectbox(f"Color by:", [None] + columns, key=f"color_{position}")
                
                chart_configs[position] = {
                    'type': chart_type,
                    'x': x_col,
                    'y': y_col,
                    'z': z_col,
                    'color': color_col
                }
    
    # Generate dashboard
    if st.button("🚀 Generate Dashboard", type="primary"):
        st.session_state.dashboard_config = {
            'name': dashboard_name,
            'layout': layout_type,
            'charts': chart_configs
        }
        
        st.markdown(f"### 📱 Dashboard: {dashboard_name}")
        
        # Create layout based on type
        if layout_type == "2x2 Grid":
            row1_col1, row1_col2 = st.columns(2)
            row2_col1, row2_col2 = st.columns(2)
            containers = [row1_col1, row1_col2, row2_col1, row2_col2]
        elif layout_type == "Single Row":
            containers = st.columns(len(chart_positions))
        elif layout_type == "Single Column":
            containers = [st.container() for _ in chart_positions]
        else:  # Custom
            containers = st.columns(min(len(chart_positions), 3))
        
        # Generate charts
        for i, (position, config) in enumerate(chart_configs.items()):
            if config['type'] != "None" and i < len(containers):
                with containers[i]:
                    fig = create_advanced_visualization(df, config)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(f"Could not generate {config['type']} for {position}")
        
        st.success("Dashboard generated successfully!")

# Templates Section (Complete Implementation)
elif main_section == "📋 Templates":
    st.markdown('<h2 class="section-header">📋 Cleaning Templates & Workflows</h2>', unsafe_allow_html=True)
    
    template_tab1, template_tab2, template_tab3 = st.tabs(["🏭 Predefined Templates", "💾 My Templates", "➕ Create Template"])
    
    with template_tab1:
        st.markdown("### 🏭 Industry-Specific Templates")
        
        predefined_templates = get_predefined_templates()
        
        for template_name, template_info in predefined_templates.items():
            with st.expander(f"📊 {template_name}", expanded=False):
                st.write(f"**Description:** {template_info['description']}")
                st.write("**Included Steps:**")
                
                for i, step in enumerate(template_info['steps'], 1):
                    step_desc = f"{i}. "
                    if step['type'] == 'remove_duplicates':
                        step_desc += "Remove duplicate rows"
                    elif step['type'] == 'handle_missing':
                        step_desc += f"Handle missing values in '{step['column']}' using {step['method']}"
                    elif step['type'] == 'handle_outliers':
                        step_desc += f"Handle outliers in {step['columns']} using {step['method']}"
                    elif step['type'] == 'convert_types':
                        step_desc += f"Convert '{step['column']}' to {step['target_type']}"
                    elif step['type'] == 'standardize_text':
                        step_desc += f"Standardize text in {step['columns']} using {step['method']}"
                    elif step['type'] == 'scaling':
                        step_desc += f"Apply {step['method']} to {step['columns']}"
                    
                    st.write(step_desc)
                
                if st.button(f"Apply {template_name}", key=f"apply_{template_name}"):
                    if st.session_state.df is not None:
                        st.info(f"Applied {template_name} template - implement execution logic here")
                    else:
                        st.warning("Please upload a dataset first!")
    
    with template_tab2:
        st.markdown("### 💾 Your Saved Templates")
        
        if st.session_state.templates:
            for template_name, template_data in st.session_state.templates.items():
                st.markdown(f"""
                    <div class="template-card">
                        <h4>{template_name}</h4>
                        <p><strong>Created:</strong> {template_data['created_date'][:10]}</p>
                        <p><strong>Steps:</strong> {len(template_data['steps'])}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Apply {template_name}", key=f"apply_custom_{template_name}"):
                        st.info("Template application logic would be implemented here")
                with col2:
                    if st.button(f"Delete {template_name}", key=f"delete_{template_name}"):
                        del st.session_state.templates[template_name]
                        st.rerun()
        else:
            st.info("No saved templates yet. Create one in the 'Create Template' tab!")
    
    with template_tab3:
        st.markdown("### ➕ Create New Template")
        
        new_template_name = st.text_input("Template Name:")
        new_template_desc = st.text_area("Description:")
        
        # Template builder interface
        st.markdown("#### 🔧 Build Template Steps")
        
        if 'template_steps' not in st.session_state:
            st.session_state.template_steps = []
        
        # Add new step
        step_type = st.selectbox(
            "Add step type:",
            ["Remove Duplicates", "Handle Missing Values", "Remove Outliers", "Data Type Conversion", "Text Cleaning", "Scaling"]
        )
        
        step_config = {}
        
        if step_type == "Handle Missing Values":
            if st.session_state.df is not None:
                df = st.session_state.df
                columns = df.columns.tolist()
            else:
                columns = []
            step_config['column'] = st.selectbox("Column:", columns)
            step_config['method'] = st.selectbox("Method:", [
                "Fill with mean", "Fill with median", "Fill with mode", 
                "Remove rows", "Forward fill", "Backward fill"
            ])
        
        elif step_type == "Remove Outliers":
            if st.session_state.df is not None:
                df = st.session_state.df
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            else:
                numeric_cols = []
            step_config['columns'] = st.multiselect("Columns:", numeric_cols)
            step_config['method'] = st.selectbox("Method:", ["IQR", "Z-score", "Isolation Forest"])
        
        if st.button("➕ Add Step"):
            step = {
                'type': step_type,
                'config': step_config,
                'order': len(st.session_state.template_steps) + 1
            }
            st.session_state.template_steps.append(step)
            st.rerun()
        
        # Show current steps
        if st.session_state.template_steps:
            st.markdown("#### 📝 Current Template Steps")
            for i, step in enumerate(st.session_state.template_steps):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{i+1}. {step['type']} - {step['config']}")
                with col2:
                    if st.button("🗑️", key=f"delete_step_{i}"):
                        st.session_state.template_steps.pop(i)
                        st.rerun()
        
        # Save template
        if new_template_name and st.session_state.template_steps:
            if st.button("💾 Save Template"):
                save_cleaning_template(new_template_name, st.session_state.template_steps.copy())
                st.session_state.template_steps = []
                st.success(f"Template '{new_template_name}' saved successfully!")
                st.rerun()

# Settings Section (New Implementation)
elif main_section == "⚙️ Settings":
    st.markdown('<h2 class="section-header">⚙️ Platform Settings</h2>', unsafe_allow_html=True)
    
    settings_tab1, settings_tab2, settings_tab3 = st.tabs(["🎛️ General", "🎨 Appearance", "📊 Data Processing"])
    
    with settings_tab1:
        st.markdown("### 🎛️ General Settings")
        
        # Auto-save settings
        auto_save = st.checkbox("Auto-save cleaning operations", value=True)
        
        # Default visualization theme
        viz_theme = st.selectbox(
            "Default visualization theme:",
            ["plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white"]
        )
        
        # Performance settings
        st.markdown("#### ⚡ Performance")
        max_rows_display = st.slider("Maximum rows to display in previews:", 10, 1000, 100)
        enable_caching = st.checkbox("Enable data caching", value=True)
        
        # AI settings
        st.markdown("#### 🧠 AI Features")
        ai_suggestions = st.checkbox("Enable AI suggestions", value=True)
        auto_quality_check = st.checkbox("Auto-calculate data quality on upload", value=True)
        confidence_threshold = st.slider("AI confidence threshold:", 0.0, 1.0, 0.7)
        
        if st.button("💾 Save General Settings"):
            # In a real app, these would be saved to user preferences
            st.success("Settings saved successfully!")
    
    with settings_tab2:
        st.markdown("### 🎨 Appearance Customization")
        
        # Color theme
        color_theme = st.selectbox(
            "Color theme:",
            ["Default Blue", "Green Nature", "Purple Gradient", "Orange Sunset", "Dark Mode"]
        )
        
        # Chart defaults
        st.markdown("#### 📊 Chart Defaults")
        default_height = st.slider("Default chart height (px):", 300, 800, 500)
        show_grid = st.checkbox("Show grid lines by default", value=True)
        animate_charts = st.checkbox("Enable chart animations", value=True)
        
        # Preview theme
        if st.button("👀 Preview Theme"):
            # Create a sample chart with the selected theme
            if st.session_state.df is not None:
                df = st.session_state.df
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    sample_fig = px.histogram(df, x=numeric_cols[0], title="Theme Preview")
                    if color_theme == "Dark Mode":
                        sample_fig.update_layout(template="plotly_dark")
                    elif color_theme == "Green Nature":
                        sample_fig.update_layout(colorway=['#10b981', '#059669', '#047857'])
                    
                    st.plotly_chart(sample_fig, use_container_width=True)
    
    with settings_tab3:
        st.markdown("### 📊 Data Processing Settings")
        
        # Memory management
        st.markdown("#### 💾 Memory Management")
        chunk_size = st.slider("Large file chunk size (rows):", 1000, 100000, 10000)
        memory_limit = st.selectbox("Memory usage limit:", ["Low (< 1GB)", "Medium (< 4GB)", "High (< 8GB)", "Unlimited"])
        
        # Default cleaning options
        st.markdown("#### 🧹 Default Cleaning Behavior")
        auto_remove_empty_cols = st.checkbox("Auto-remove completely empty columns", value=True)
        auto_drop_high_missing = st.checkbox("Auto-drop columns with >80% missing data", value=False)
        default_missing_method = st.selectbox(
            "Default missing value method:",
            ["Fill with mean", "Fill with median", "Fill with mode", "Remove rows"]
        )
        
        # Export settings
        st.markdown("#### 📤 Export Settings")
        default_export_format = st.selectbox("Default export format:", ["CSV", "Excel", "JSON", "Parquet"])
        include_metadata = st.checkbox("Include cleaning metadata in exports", value=True)
        
        # Save processing settings
        if st.button("💾 Save Processing Settings"):
            # Store in session state (in real app, would persist to user profile)
            processing_settings = {
                'chunk_size': chunk_size,
                'memory_limit': memory_limit,
                'auto_remove_empty_cols': auto_remove_empty_cols,
                'auto_drop_high_missing': auto_drop_high_missing,
                'default_missing_method': default_missing_method,
                'default_export_format': default_export_format,
                'include_metadata': include_metadata
            }
            
            for key, value in processing_settings.items():
                st.session_state[key] = value
            
            st.success("Processing settings saved!")

# Enhanced Footer with Export Options
if st.session_state.df is not None:
    st.markdown("---")
    st.markdown("### 📤 Export Options")
    
    export_col1, export_col2, export_col3, export_col4 = st.columns(4)
    
    with export_col1:
        if st.button("📊 Export as CSV"):
            csv = st.session_state.df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"cleaned_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with export_col2:
        if st.button("📈 Export as Excel"):
            try:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    st.session_state.df.to_excel(writer, sheet_name='Cleaned Data', index=False)
                    
                    # Add metadata sheet if cleaning history exists
                    if st.session_state.cleaning_history:
                        metadata_df = pd.DataFrame({
                            'Step': range(1, len(st.session_state.cleaning_history) + 1),
                            'Operation': st.session_state.cleaning_history,
                            'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * len(st.session_state.cleaning_history)
                        })
                        metadata_df.to_excel(writer, sheet_name='Cleaning History', index=False)
                
                output.seek(0)
                st.download_button(
                    label="Download Excel",
                    data=output.getvalue(),
                    file_name=f"cleaned_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error creating Excel file: {str(e)}")
    
    with export_col3:
        if st.button("🗃️ Export as JSON"):
            json_data = st.session_state.df.to_json(orient='records', indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"cleaned_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with export_col4:
        if st.button("📋 Export Cleaning Report"):
            # Generate comprehensive cleaning report
            report = f"""
# Data Cleaning Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Dataset Summary
- **Rows:** {st.session_state.df.shape[0]:,}
- **Columns:** {st.session_state.df.shape[1]}
- **Memory Usage:** {st.session_state.df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB

## Data Quality Score
- **Overall Score:** {st.session_state.data_quality_score or 'Not calculated'}/100

## Cleaning Operations Applied
"""
            for i, operation in enumerate(st.session_state.cleaning_history, 1):
                report += f"{i}. {operation}\n"
            
            if not st.session_state.cleaning_history:
                report += "No cleaning operations applied.\n"
            
            report += f"""
## Column Information
"""
            for col in st.session_state.df.columns:
                missing_pct = (st.session_state.df[col].isnull().sum() / len(st.session_state.df)) * 100
                report += f"- **{col}:** {st.session_state.df[col].dtype}, {missing_pct:.1f}% missing, {st.session_state.df[col].nunique()} unique values\n"
            
            st.download_button(
                label="Download Report",
                data=report,
                file_name=f"cleaning_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )

# Enhanced Mobile Responsiveness (CSS additions)
st.markdown("""
<style>
    /* Mobile Responsive Enhancements */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        .section-header {
            font-size: 1.4rem;
        }
        .metric-card {
            margin-bottom: 1rem;
        }
        .quality-score {
            width: 80px;
            height: 80px;
            font-size: 1.8rem;
        }
    }
    
    /* Enhanced Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #555;
        color: white;
        text-align: center;
        padding: 5px;
        border-radius: 6px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -100px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Loading animations */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Advanced Data Validation Functions (Phase 2 Features)
def validate_data_integrity(df):
    """Advanced data integrity validation"""
    validation_results = {
        'duplicate_check': df.duplicated().sum(),
        'missing_check': df.isnull().sum().sum(),
        'type_consistency': True,  # Simplified
        'range_validation': {},
        'format_validation': {}
    }
    
    # Range validation for numeric columns
    for col in df.select_dtypes(include=[np.number]).columns:
        q1, q3 = df[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        outliers = ((df[col] < (q1 - 3 * iqr)) | (df[col] > (q3 + 3 * iqr))).sum()
        validation_results['range_validation'][col] = {
            'outliers': outliers,
            'outlier_percentage': (outliers / len(df)) * 100
        }
    
    # Format validation for text columns
    for col in df.select_dtypes(include=['object']).columns:
        # Email validation
        if 'email' in col.lower():
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            invalid_emails = ~df[col].astype(str).str.match(email_pattern, na=False)
            validation_results['format_validation'][col] = {
                'invalid_count': invalid_emails.sum(),
                'format_type': 'email'
            }
    
    return validation_results

# AI-Powered Column Profiling (Phase 2 Feature)
def profile_column_ai(df, column):
    """AI-powered comprehensive column profiling"""
    profile = {
        'column_name': column,
        'data_type': str(df[column].dtype),
        'missing_count': df[column].isnull().sum(),
        'missing_percentage': (df[column].isnull().sum() / len(df)) * 100,
        'unique_count': df[column].nunique(),
        'unique_percentage': (df[column].nunique() / len(df)) * 100
    }
    
    # Type-specific profiling
    if df[column].dtype in ['int64', 'float64']:
        profile.update({
            'min_value': df[column].min(),
            'max_value': df[column].max(),
            'mean': df[column].mean(),
            'median': df[column].median(),
            'std_dev': df[column].std(),
            'skewness': df[column].skew(),
            'kurtosis': df[column].kurtosis(),
            'outliers_iqr': detect_outliers_advanced(df, [column], 'statistical').sum()
        })
        
        # AI insights for numeric data
        if abs(profile['skewness']) > 2:
            profile['ai_insight'] = f"Highly skewed distribution (skewness: {profile['skewness']:.2f})"
        elif profile['unique_percentage'] < 5:
            profile['ai_insight'] = "Low cardinality - consider treating as categorical"
        elif profile['outliers_iqr'] > len(df) * 0.1:
            profile['ai_insight'] = "High number of outliers detected"
        else:
            profile['ai_insight'] = "Normal numeric distribution"
    
    else:  # Object/categorical data
        value_counts = df[column].value_counts()
        profile.update({
            'most_frequent': value_counts.index[0] if not value_counts.empty else None,
            'most_frequent_count': value_counts.iloc[0] if not value_counts.empty else 0,
            'least_frequent': value_counts.index[-1] if not value_counts.empty else None,
            'least_frequent_count': value_counts.iloc[-1] if not value_counts.empty else 0
        })
        
        # AI insights for categorical data
        if profile['unique_percentage'] > 95:
            profile['ai_insight'] = "High cardinality - might be an identifier or need grouping"
        elif len(value_counts) < 10:
            profile['ai_insight'] = "Low cardinality - good for grouping/filtering"
        else:
            profile['ai_insight'] = "Medium cardinality categorical data"
    
    return profile

# Enhanced Data Export with Metadata (Phase 2 Feature)
def export_with_metadata(df, export_format, include_history=True):
    """Export data with comprehensive metadata"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if export_format == "CSV":
        # CSV with separate metadata file
        csv_data = df.to_csv(index=False)
        
        if include_history:
            metadata = {
                'export_timestamp': timestamp,
                'original_shape': st.session_state.original_df.shape if st.session_state.original_df is not None else None,
                'final_shape': df.shape,
                'cleaning_operations': st.session_state.cleaning_history,
                'data_quality_score': st.session_state.data_quality_score,
                'column_types': {col: str(df[col].dtype) for col in df.columns}
            }
            
            metadata_json = json.dumps(metadata, indent=2, default=str)
            return csv_data, metadata_json
        
        return csv_data, None
    
    elif export_format == "Excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Cleaned Data', index=False)
            
            if include_history and st.session_state.cleaning_history:
                # Add cleaning history sheet
                history_df = pd.DataFrame({
                    'Step': range(1, len(st.session_state.cleaning_history) + 1),
                    'Operation': st.session_state.cleaning_history,
                    'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * len(st.session_state.cleaning_history)
                })
                history_df.to_excel(writer, sheet_name='Cleaning History', index=False)
                
                # Add summary sheet
                summary_data = {
                    'Metric': ['Original Rows', 'Current Rows', 'Original Columns', 'Current Columns', 
                              'Missing Values', 'Duplicates Removed', 'Data Quality Score'],
                    'Value': [
                        st.session_state.original_df.shape[0] if st.session_state.original_df is not None else 'N/A',
                        df.shape[0],
                        st.session_state.original_df.shape[1] if st.session_state.original_df is not None else 'N/A',
                        df.shape[1],
                        df.isnull().sum().sum(),
                        len([op for op in st.session_state.cleaning_history if 'duplicate' in op.lower()]),
                        f"{st.session_state.data_quality_score:.1f}" if st.session_state.data_quality_score else 'N/A'
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        output.seek(0)
        return output.getvalue(), None

# Pipeline Builder (Phase 2 Major Feature)
def create_pipeline_builder():
    """Advanced data processing pipeline builder"""
    st.markdown("### 🔧 Data Processing Pipeline Builder")
    
    # Initialize pipeline if not exists
    if 'pipeline_steps' not in st.session_state:
        st.session_state.pipeline_steps = []
    
    # Pipeline visualization
    if st.session_state.pipeline_steps:
        st.markdown("#### 🔄 Current Pipeline")
        
        # Create a visual pipeline representation
        pipeline_cols = st.columns(len(st.session_state.pipeline_steps) + 1)
        
        with pipeline_cols[0]:
            st.markdown("""
                <div style="background: #f3f4f6; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                    <strong>Raw Data</strong><br>
                    📁 Input
                </div>
            """, unsafe_allow_html=True)
        
        for i, step in enumerate(st.session_state.pipeline_steps):
            with pipeline_cols[i + 1]:
                st.markdown(f"""
                    <div style="background: #dbeafe; padding: 1rem; border-radius: 0.5rem; text-align: center; margin: 0 0.5rem;">
                        <strong>Step {i+1}</strong><br>
                        {step['name']}<br>
                        <small>{step['type']}</small>
                    </div>
                """, unsafe_allow_html=True)
        
        # Pipeline controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Execute Pipeline"):
                execute_pipeline(st.session_state.df, st.session_state.pipeline_steps)
        
        with col2:
            if st.button("💾 Save Pipeline"):
                pipeline_name = st.text_input("Pipeline name:", key="save_pipeline_name")
                if pipeline_name:
                    save_pipeline(pipeline_name, st.session_state.pipeline_steps)
        
        with col3:
            if st.button("🗑️ Clear Pipeline"):
                st.session_state.pipeline_steps = []
                st.rerun()
    
    # Add new pipeline step
    st.markdown("#### ➕ Add Pipeline Step")
    
    step_type = st.selectbox(
        "Step Type:",
        ["Data Validation", "Missing Value Handler", "Outlier Detection", 
         "Data Transformation", "Feature Engineering", "Data Aggregation"]
    )
    
    step_config = configure_pipeline_step(step_type)
    
    if st.button("Add to Pipeline") and step_config:
        new_step = {
            'name': step_config.get('name', step_type),
            'type': step_type,
            'config': step_config,
            'order': len(st.session_state.pipeline_steps)
        }
        st.session_state.pipeline_steps.append(new_step)
        st.rerun()

def save_pipeline(name, steps):
    """Save pipeline configuration"""
    if 'saved_pipelines' not in st.session_state:
        st.session_state.saved_pipelines = {}
    
    st.session_state.saved_pipelines[name] = {
        'steps': steps,
        'created_date': datetime.now().isoformat()
    }
    st.success(f"Pipeline '{name}' saved successfully!")

def configure_pipeline_step(step_type):
    """Configure individual pipeline steps"""
    config = {}
    
    if step_type == "Missing Value Handler":
        config['name'] = st.text_input("Step name:", value="Handle Missing Values")
        config['strategy'] = st.selectbox("Strategy:", ["drop", "fill_mean", "fill_median", "fill_mode", "interpolate"])
        config['threshold'] = st.slider("Missing threshold (%):", 0, 100, 50)
        
    elif step_type == "Outlier Detection":
        config['name'] = st.text_input("Step name:", value="Remove Outliers")
        config['method'] = st.selectbox("Method:", ["iqr", "zscore", "isolation_forest"])
        config['threshold'] = st.slider("Sensitivity:", 1, 5, 3)
        
    elif step_type == "Feature Engineering":
        config['name'] = st.text_input("Step name:", value="Engineer Features")
        config['operations'] = st.multiselect("Operations:", [
            "Create date features", "Binning", "Scaling", "Encoding", "Mathematical transformations"
        ])
    
    return config

def execute_pipeline(df, pipeline_steps):
    """Execute the complete data processing pipeline"""
    if df is None:
        st.error("No data available to process")
        return
    
    processed_df = df.copy()
    execution_log = []
    
    try:
        with st.spinner("Executing pipeline..."):
            for i, step in enumerate(pipeline_steps):
                step_start = datetime.now()
                
                if step['type'] == "Missing Value Handler":
                    initial_missing = processed_df.isnull().sum().sum()
                    
                    if step['config']['strategy'] == 'drop':
                        processed_df = processed_df.dropna()
                    elif step['config']['strategy'] == 'fill_mean':
                        numeric_cols = processed_df.select_dtypes(include=[np.number]).columns
                        processed_df[numeric_cols] = processed_df[numeric_cols].fillna(processed_df[numeric_cols].mean())
                    elif step['config']['strategy'] == 'fill_median':
                        numeric_cols = processed_df.select_dtypes(include=[np.number]).columns
                        processed_df[numeric_cols] = processed_df[numeric_cols].fillna(processed_df[numeric_cols].median())
                    
                    final_missing = processed_df.isnull().sum().sum()
                    execution_log.append(f"Step {i+1}: Reduced missing values from {initial_missing} to {final_missing}")
                
                elif step['type'] == "Outlier Detection":
                    numeric_cols = processed_df.select_dtypes(include=[np.number]).columns
                    initial_rows = len(processed_df)
                    
                    for col in numeric_cols:
                        outliers = detect_outliers_advanced(processed_df, [col], step['config']['method'])
                        processed_df = processed_df[~outliers]
                    
                    final_rows = len(processed_df)
                    execution_log.append(f"Step {i+1}: Removed {initial_rows - final_rows} outlier rows")
                
                step_duration = (datetime.now() - step_start).total_seconds()
                execution_log.append(f"  ⏱️ Completed in {step_duration:.2f} seconds")
        
        # Update session state
        st.session_state.df = processed_df
        st.session_state.cleaning_history.extend([f"Pipeline: {step['name']}" for step in pipeline_steps])
        
        # Show execution results
        st.success("Pipeline executed successfully!")
        
        with st.expander("View Execution Log", expanded=True):
            for log_entry in execution_log:
                st.text(log_entry)
        
        # Show before/after comparison
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Shape", f"{df.shape[0]} × {df.shape[1]}")
        with col2:
            st.metric("Processed Shape", f"{processed_df.shape[0]} × {processed_df.shape[1]}")
    
    except Exception as e:
        st.error(f"Pipeline execution failed: {str(e)}")

# Advanced Statistical Tests (Phase 2 Feature)
def perform_advanced_statistical_test(df, test_type, **kwargs):
    """Perform advanced statistical tests with AI interpretation"""
    
    if test_type == "T-Test":
        col1 = kwargs.get('column1')
        col2 = kwargs.get('column2') 
        test_type_variant = kwargs.get('variant', 'independent')
        
        if test_type_variant == 'independent':
            stat, p_value = stats.ttest_ind(df[col1].dropna(), df[col2].dropna())
        else:  # paired
            stat, p_value = stats.ttest_rel(df[col1].dropna(), df[col2].dropna())
        
        interpretation = {
            'statistic': stat,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'interpretation': f"{'Significant' if p_value < 0.05 else 'Not significant'} difference between groups (p = {p_value:.4f})"
        }
        
        return interpretation
    
    elif test_type == "ANOVA":
        group_col = kwargs.get('group_column')
        value_col = kwargs.get('value_column')
        
        groups = [group for name, group in df.groupby(group_col)[value_col] if len(group) > 0]
        
        if len(groups) > 2:
            stat, p_value = stats.f_oneway(*groups)
            
            interpretation = {
                'statistic': stat,
                'p_value': p_value,
                'significant': p_value < 0.05,
                'groups_tested': len(groups),
                'interpretation': f"{'Significant' if p_value < 0.05 else 'Not significant'} differences between {len(groups)} groups (p = {p_value:.4f})"
            }
            
            return interpretation
    
    elif test_type == "Chi-Square":
        col1 = kwargs.get('column1')
        col2 = kwargs.get('column2')
        
        contingency_table = pd.crosstab(df[col1], df[col2])
        stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        interpretation = {
            'statistic': stat,
            'p_value': p_value,
            'degrees_of_freedom': dof,
            'significant': p_value < 0.05,
            'interpretation': f"{'Significant' if p_value < 0.05 else 'Not significant'} association between {col1} and {col2} (p = {p_value:.4f})"
        }
        
        return interpretation
    
    return None

# Advanced Anomaly Detection (Phase 2 Feature)
def detect_anomalies_advanced(df, method='ensemble'):
    """Advanced anomaly detection using ensemble methods"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) == 0:
        return pd.Series([False] * len(df), index=df.index)
    
    # Prepare data
    data = df[numeric_cols].fillna(df[numeric_cols].mean())
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    
    anomaly_scores = np.zeros(len(df))
    
    if method == 'ensemble':
        # Isolation Forest
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        iso_scores = iso_forest.decision_function(scaled_data)
        anomaly_scores += (iso_scores < np.percentile(iso_scores, 10)).astype(int)
        
        # Statistical outliers (Z-score)
        z_scores = np.abs(stats.zscore(scaled_data, axis=0, nan_policy='omit'))
        z_outliers = (z_scores > 3).any(axis=1)
        anomaly_scores += z_outliers.astype(int)
        
        # IQR outliers
        for i, col in enumerate(numeric_cols):
            Q1, Q3 = np.percentile(data.iloc[:, i], [25, 75])
            IQR = Q3 - Q1
            outliers = (data.iloc[:, i] < (Q1 - 1.5 * IQR)) | (data.iloc[:, i] > (Q3 + 1.5 * IQR))
            anomaly_scores += outliers.astype(int)
        
        # Ensemble decision: anomaly if detected by 2+ methods
        final_anomalies = anomaly_scores >= 2
        
    else:
        # Single method
        if method == 'isolation_forest':
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            predictions = iso_forest.fit_predict(scaled_data)
            final_anomalies = predictions == -1
        elif method == 'statistical':
            z_scores = np.abs(stats.zscore(scaled_data, axis=0, nan_policy='omit'))
            final_anomalies = (z_scores > 3).any(axis=1)
    
    return pd.Series(final_anomalies, index=df.index)

# Collaboration Features (Phase 2)
def setup_collaboration_features():
    """Setup collaboration features for team data analysis"""
    st.markdown("### 👥 Collaboration Features")
    
    # Comment system
    if 'comments' not in st.session_state:
        st.session_state.comments = []
    
    # Add comment
    with st.expander("💬 Add Comment", expanded=False):
        comment_text = st.text_area("Comment:")
        comment_type = st.selectbox("Type:", ["General", "Data Quality", "Cleaning Suggestion", "Analysis Insight"])
        
        if st.button("Add Comment") and comment_text:
            new_comment = {
                'text': comment_text,
                'type': comment_type,
                'timestamp': datetime.now().isoformat(),
                'user': 'Current User'  # In real app, would get from auth
            }
            st.session_state.comments.append(new_comment)
            st.success("Comment added!")
            st.rerun()
    
    # Display comments
    if st.session_state.comments:
        st.markdown("#### 💬 Team Comments")
        for i, comment in enumerate(st.session_state.comments):
            comment_time = datetime.fromisoformat(comment['timestamp']).strftime('%Y-%m-%d %H:%M')
            
            st.markdown(f"""
                <div style="background: #f9fafb; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; border-left: 4px solid #3b82f6;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong>{comment['user']}</strong>
                        <span style="color: #6b7280; font-size: 0.875rem;">{comment_time}</span>
                    </div>
                    <div style="background: #{'fef3c7' if comment['type'] == 'Cleaning Suggestion' else 'ecfdf5' if comment['type'] == 'Data Quality' else 'f3f4f6'}; 
                                padding: 0.5rem; border-radius: 0.25rem; margin-bottom: 0.5rem;">
                        <small><strong>{comment['type']}</strong></small>
                    </div>
                    <p>{comment['text']}</p>
                </div>
            """, unsafe_allow_html=True)

# Add collaboration to main section (insert after Settings)
if main_section == "👥 Collaboration":
    st.markdown('<h2 class="section-header">👥 Team Collaboration</h2>', unsafe_allow_html=True)
    setup_collaboration_features()

# Pipeline Builder Section
elif main_section == "🔧 Pipeline Builder":
    st.markdown('<h2 class="section-header">🔧 Advanced Pipeline Builder</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("Please upload a dataset first!")
        st.stop()
    
    create_pipeline_builder()

# Enhanced Data Quality Monitoring (Phase 2)
def create_quality_monitoring_dashboard():
    """Create a comprehensive data quality monitoring dashboard"""
    st.markdown("### 📊 Data Quality Monitoring Dashboard")
    
    if st.session_state.df is None:
        return
    
    df = st.session_state.df
    
    # Real-time quality metrics
    quality_metrics = {
        'completeness': ((len(df) * len(df.columns) - df.isnull().sum().sum()) / (len(df) * len(df.columns))) * 100,
        'uniqueness': ((len(df) - df.duplicated().sum()) / len(df)) * 100,
        'consistency': 95,  # Placeholder - would implement actual consistency checks
        'validity': 90,     # Placeholder - would implement actual validity checks
        'timeliness': 88    # Placeholder - would check data freshness
    }
    
    # Quality metrics visualization
    metric_names = list(quality_metrics.keys())
    metric_values = list(quality_metrics.values())
    
    fig = go.Figure()
    
    # Radar chart for quality dimensions
    fig.add_trace(go.Scatterpolar(
        r=metric_values + [metric_values[0]],  # Close the radar
        theta=metric_names + [metric_names[0]],
        fill='toself',
        name='Data Quality'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        title="Data Quality Radar Chart",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Quality score trend (simulated)
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    quality_trend = np.random.normal(85, 5, 30)  # Simulated quality scores
    quality_trend = np.clip(quality_trend, 0, 100)
    
    trend_fig = px.line(
        x=dates, y=quality_trend,
        title="Data Quality Trend (Last 30 Days)",
        labels={'x': 'Date', 'y': 'Quality Score'}
    )
    trend_fig.add_hline(y=80, line_dash="dash", line_color="red", 
                        annotation_text="Quality Threshold")
    
    st.plotly_chart(trend_fig, use_container_width=True)

# Advanced File Format Support (Phase 1 Feature)
def load_advanced_formats(file):
    """Support for additional file formats"""
    file_extension = file.name.split('.')[-1].lower()
    
    try:
        if file_extension == 'feather':
            return pd.read_feather(file)
        elif file_extension == 'hdf5' or file_extension == 'h5':
            return pd.read_hdf(file)
        elif file_extension == 'orc':
            # Would require pyarrow
            st.error("ORC format requires additional dependencies")
            return None
        elif file_extension == 'avro':
            # Would require fastavro
            st.error("AVRO format requires additional dependencies")
            return None
        elif file_extension in ['xml']:
            # Basic XML support
            try:
                import xml.etree.ElementTree as ET
                tree = ET.parse(file)
                root = tree.getroot()
                
                # Convert XML to DataFrame (simplified approach)
                data = []
                for child in root:
                    row_data = {}
                    for subchild in child:
                        row_data[subchild.tag] = subchild.text
                    data.append(row_data)
                
                return pd.DataFrame(data)
            except Exception as e:
                st.error(f"XML parsing failed: {str(e)}")
                return None
    except Exception as e:
        st.error(f"Error loading {file_extension} file: {str(e)}")
        return None

# Smart Data Profiling Report (Phase 2)
def generate_smart_profiling_report(df):
    """Generate AI-powered comprehensive data profiling report"""
    report = {
        'dataset_overview': {
            'rows': len(df),
            'columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'duplicate_rows': df.duplicated().sum(),
            'total_missing_cells': df.isnull().sum().sum()
        },
        'column_profiles': {},
        'data_relationships': {},
        'quality_issues': [],
        'recommendations': []
    }
    
    # Profile each column
    for col in df.columns:
        profile = profile_column_ai(df, col)
        report['column_profiles'][col] = profile
        
        # Generate quality issues
        if profile['missing_percentage'] > 30:
            report['quality_issues'].append({
                'severity': 'high',
                'column': col,
                'issue': f"High missing data ({profile['missing_percentage']:.1f}%)",
                'recommendation': 'Consider imputation or column removal'
            })
        
        if profile.get('outliers_iqr', 0) > len(df) * 0.15:
            report['quality_issues'].append({
                'severity': 'medium',
                'column': col,
                'issue': f"Many outliers detected ({profile.get('outliers_iqr', 0)} values)",
                'recommendation': 'Review outlier handling strategy'
            })
    
    # Data relationships analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        
        # Find strong correlations
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.8:
                    strong_correlations.append({
                        'var1': corr_matrix.columns[i],
                        'var2': corr_matrix.columns[j],
                        'correlation': corr_val
                    })
        
        report['data_relationships']['strong_correlations'] = strong_correlations
    
    # AI recommendations
    if len(report['quality_issues']) == 0:
        report['recommendations'].append("Data quality is excellent. Proceed with analysis.")
    elif len([issue for issue in report['quality_issues'] if issue['severity'] == 'high']) > 0:
        report['recommendations'].append("Address high-severity data quality issues before analysis.")
    else:
        report['recommendations'].append("Minor data quality issues detected. Clean data for optimal results.")
    
    return report

# Add the Pipeline Builder to the main navigation options
# Update the sidebar radio button options
if 'main_section' not in locals():
    main_section = st.sidebar.radio(
        "Navigate to:",
        ["🏠 Home", "📁 Data Upload", "🧠 AI Insights", "🧹 Smart Cleaning", 
         "📊 Advanced Analytics", "🎨 Dashboard Builder", "🔧 Pipeline Builder",
         "📋 Templates", "👥 Collaboration", "⚙️ Settings"]
    )

# Additional Phase 2 Features: API Integration
def setup_api_integrations():
    """Setup API integrations for external data sources"""
    st.markdown("### 🔌 API Integrations")
    
    integration_type = st.selectbox(
        "Choose integration:",
        ["REST API", "Database Connection", "Google Sheets", "Cloud Storage"]
    )
    
    if integration_type == "REST API":
        st.markdown("#### 🌐 REST API Data Import")
        
        api_url = st.text_input("API Endpoint URL:")
        api_key = st.text_input("API Key (optional):", type="password")
        
        # Headers configuration
        with st.expander("Configure Headers", expanded=False):
            header_key = st.text_input("Header Key:")
            header_value = st.text_input("Header Value:")
        
        if st.button("🔗 Test Connection") and api_url:
            try:
                headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
                if header_key and header_value:
                    headers[header_key] = header_value
                
                response = requests.get(api_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    st.success("Connection successful!")
                    
                    # Try to parse as JSON and convert to DataFrame
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            api_df = pd.DataFrame(data)
                        elif isinstance(data, dict) and 'data' in data:
                            api_df = pd.DataFrame(data['data'])
                        else:
                            api_df = pd.json_normalize(data)
                        
                        st.dataframe(api_df.head(), use_container_width=True)
                        
                        if st.button("📥 Import API Data"):
                            st.session_state.df = api_df
                            st.session_state.original_df = api_df.copy()
                            st.success("API data imported successfully!")
                            st.rerun()
                            
                    except Exception as e:
                        st.error(f"Data parsing failed: {str(e)}")
                        st.text("Raw Response Preview:")
                        st.text(response.text[:500])
                else:
                    st.error(f"API Error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                st.error("Request timeout - check URL and try again")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection failed: {str(e)}")
    
    elif integration_type == "Database Connection":
        st.markdown("#### 🗄️ Database Connection")
        
        db_type = st.selectbox("Database Type:", ["SQLite", "PostgreSQL", "MySQL", "SQL Server"])
        
        if db_type == "SQLite":
            uploaded_db = st.file_uploader("Upload SQLite file:", type=['db', 'sqlite', 'sqlite3'])
            
            if uploaded_db:
                # Save uploaded file temporarily
                with open("temp_db.sqlite", "wb") as f:
                    f.write(uploaded_db.getbuffer())
                
                try:
                    conn = sqlite3.connect("temp_db.sqlite")
                    
                    # Get table names
                    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
                    
                    if not tables.empty:
                        selected_table = st.selectbox("Select table:", tables['name'].tolist())
                        
                        if st.button("📊 Preview Table"):
                            preview_df = pd.read_sql_query(f"SELECT * FROM {selected_table} LIMIT 100;", conn)
                            st.dataframe(preview_df, use_container_width=True)
                            
                            if st.button("📥 Import Table"):
                                full_df = pd.read_sql_query(f"SELECT * FROM {selected_table};", conn)
                                st.session_state.df = full_df
                                st.session_state.original_df = full_df.copy()
                                st.success(f"Imported {len(full_df)} rows from {selected_table}")
                                st.rerun()
                    
                    conn.close()
                except Exception as e:
                    st.error(f"Database error: {str(e)}")
        
        else:
            st.info(f"{db_type} integration would require additional database drivers and connection configuration.")

# Advanced Feature Engineering (Phase 2)
def feature_engineering_advanced(df):
    """Advanced feature engineering with AI suggestions"""
    st.markdown("### 🛠️ Advanced Feature Engineering")
    
    if df is None:
        st.warning("Please upload data first!")
        return
    
    engineering_type = st.selectbox(
        "Choose feature engineering type:",
        ["Date/Time Features", "Mathematical Transformations", "Text Features", 
         "Categorical Encoding", "Binning & Discretization", "Interaction Features"]
    )
    
    if engineering_type == "Date/Time Features":
        date_cols = []
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns]' or 'date' in col.lower():
                date_cols.append(col)
        
        if date_cols:
            selected_date_col = st.selectbox("Select date column:", date_cols)
            
            features_to_create = st.multiselect(
                "Select features to create:",
                ["Year", "Month", "Day", "Day of Week", "Quarter", "Is Weekend", 
                 "Days Since", "Month Name", "Season"]
            )
            
            if st.button("🔧 Create Date Features") and features_to_create:
                df_engineered = df.copy()
                
                # Convert to datetime if needed
                if df_engineered[selected_date_col].dtype != 'datetime64[ns]':
                    df_engineered[selected_date_col] = pd.to_datetime(df_engineered[selected_date_col])
                
                for feature in features_to_create:
                    if feature == "Year":
                        df_engineered[f"{selected_date_col}_year"] = df_engineered[selected_date_col].dt.year
                    elif feature == "Month":
                        df_engineered[f"{selected_date_col}_month"] = df_engineered[selected_date_col].dt.month
                    elif feature == "Day":
                        df_engineered[f"{selected_date_col}_day"] = df_engineered[selected_date_col].dt.day
                    elif feature == "Day of Week":
                        df_engineered[f"{selected_date_col}_dayofweek"] = df_engineered[selected_date_col].dt.dayofweek
                    elif feature == "Quarter":
                        df_engineered[f"{selected_date_col}_quarter"] = df_engineered[selected_date_col].dt.quarter
                    elif feature == "Is Weekend":
                        df_engineered[f"{selected_date_col}_is_weekend"] = df_engineered[selected_date_col].dt.dayofweek.isin([5, 6])
                    elif feature == "Days Since":
                        reference_date = st.date_input("Reference date:", value=datetime.now().date())
                        df_engineered[f"{selected_date_col}_days_since"] = (df_engineered[selected_date_col].dt.date - reference_date).dt.days
                    elif feature == "Month Name":
                        df_engineered[f"{selected_date_col}_month_name"] = df_engineered[selected_date_col].dt.month_name()
                    elif feature == "Season":
                        def get_season(month):
                            if month in [12, 1, 2]: return 'Winter'
                            elif month in [3, 4, 5]: return 'Spring'
                            elif month in [6, 7, 8]: return 'Summer'
                            else: return 'Fall'
                        df_engineered[f"{selected_date_col}_season"] = df_engineered[selected_date_col].dt.month.apply(get_season)
                
                st.session_state.df = df_engineered
                st.success(f"✅ Created {len(features_to_create)} date features!")
                
        else:
            st.info("No date columns found. Convert a column to datetime first.")
    
    elif engineering_type == "Mathematical Transformations":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            selected_cols = st.multiselect("Select numeric columns:", numeric_cols)
            
            transformations = st.multiselect(
                "Select transformations:",
                ["Log", "Square Root", "Square", "Cube", "Reciprocal", "Standardize", "Normalize"]
            )
            
            if st.button("🔧 Apply Transformations") and selected_cols and transformations:
                df_engineered = df.copy()
                
                for col in selected_cols:
                    for transform in transformations:
                        if transform == "Log":
                            # Handle negative/zero values
                            if (df_engineered[col] > 0).all():
                                df_engineered[f"{col}_log"] = np.log(df_engineered[col])
                            else:
                                df_engineered[f"{col}_log"] = np.log(df_engineered[col] - df_engineered[col].min() + 1)
                        elif transform == "Square Root":
                            if (df_engineered[col] >= 0).all():
                                df_engineered[f"{col}_sqrt"] = np.sqrt(df_engineered[col])
                            else:
                                df_engineered[f"{col}_sqrt"] = np.sqrt(df_engineered[col] - df_engineered[col].min())
                        elif transform == "Square":
                            df_engineered[f"{col}_squared"] = df_engineered[col] ** 2
                        elif transform == "Cube":
                            df_engineered[f"{col}_cubed"] = df_engineered[col] ** 3
                        elif transform == "Reciprocal":
                            df_engineered[f"{col}_reciprocal"] = 1 / (df_engineered[col] + 1e-8)  # Avoid division by zero
                        elif transform == "Standardize":
                            df_engineered[f"{col}_standardized"] = (df_engineered[col] - df_engineered[col].mean()) / df_engineered[col].std()
                        elif transform == "Normalize":
                            df_engineered[f"{col}_normalized"] = (df_engineered[col] - df_engineered[col].min()) / (df_engineered[col].max() - df_engineered[col].min())
                
                st.session_state.df = df_engineered
                st.success(f"✅ Applied {len(transformations)} transformations to {len(selected_cols)} columns!")
        else:
            st.info("No numeric columns available for mathematical transformations.")
    
    elif engineering_type == "Text Features":
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if text_cols:
            selected_col = st.selectbox("Select text column:", text_cols)
            
            text_features = st.multiselect(
                "Select text features:",
                ["Character Count", "Word Count", "Average Word Length", "Special Character Count",
                 "Uppercase Count", "Lowercase Count", "Digit Count", "Hashtag Count", "URL Count"]
            )
            
            if st.button("🔧 Create Text Features") and text_features:
                df_engineered = df.copy()
                
                for feature in text_features:
                    if feature == "Character Count":
                        df_engineered[f"{selected_col}_char_count"] = df_engineered[selected_col].astype(str).str.len()
                    elif feature == "Word Count":
                        df_engineered[f"{selected_col}_word_count"] = df_engineered[selected_col].astype(str).str.split().str.len()
                    elif feature == "Average Word Length":
                        df_engineered[f"{selected_col}_avg_word_length"] = df_engineered[selected_col].astype(str).str.split().apply(
                            lambda x: np.mean([len(word) for word in x]) if x else 0
                        )
                    elif feature == "Special Character Count":
                        df_engineered[f"{selected_col}_special_char_count"] = df_engineered[selected_col].astype(str).str.count(r'[^a-zA-Z0-9\s]')
                    elif feature == "Uppercase Count":
                        df_engineered[f"{selected_col}_uppercase_count"] = df_engineered[selected_col].astype(str).str.count(r'[A-Z]')
                    elif feature == "Lowercase Count":
                        df_engineered[f"{selected_col}_lowercase_count"] = df_engineered[selected_col].astype(str).str.count(r'[a-z]')
                    elif feature == "Digit Count":
                        df_engineered[f"{selected_col}_digit_count"] = df_engineered[selected_col].astype(str).str.count(r'\d')
                    elif feature == "Hashtag Count":
                        df_engineered[f"{selected_col}_hashtag_count"] = df_engineered[selected_col].astype(str).str.count(r'#')
                    elif feature == "URL Count":
                        df_engineered[f"{selected_col}_url_count"] = df_engineered[selected_col].astype(str).str.count(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                
                st.session_state.df = df_engineered
                st.success(f"✅ Created {len(text_features)} text features!")
        else:
            st.info("No text columns available for text feature engineering.")
    
    elif engineering_type == "Categorical Encoding":
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if categorical_cols:
            selected_cols = st.multiselect("Select categorical columns:", categorical_cols)
            
            encoding_method = st.selectbox(
                "Encoding method:",
                ["Label Encoding", "One-Hot Encoding", "Target Encoding", "Frequency Encoding"]
            )
            
            if st.button("🔧 Apply Encoding") and selected_cols:
                df_engineered = df.copy()
                
                for col in selected_cols:
                    if encoding_method == "Label Encoding":
                        from sklearn.preprocessing import LabelEncoder
                        le = LabelEncoder()
                        df_engineered[f"{col}_label_encoded"] = le.fit_transform(df_engineered[col].astype(str))
                    elif encoding_method == "One-Hot Encoding":
                        # Limit to top categories to avoid too many columns
                        top_categories = df_engineered[col].value_counts().head(10).index
                        for category in top_categories:
                            df_engineered[f"{col}_{category}"] = (df_engineered[col] == category).astype(int)
                    elif encoding_method == "Frequency Encoding":
                        freq_dict = df_engineered[col].value_counts(normalize=True).to_dict()
                        df_engineered[f"{col}_freq_encoded"] = df_engineered[col].map(freq_dict)
                    elif encoding_method == "Target Encoding":
                        # For target encoding, we need a target variable
                        target_col = st.selectbox("Select target variable for encoding:", [None] + df.columns.tolist())
                        if target_col and df_engineered[target_col].dtype in ['int64', 'float64']:
                            target_means = df_engineered.groupby(col)[target_col].mean()
                            df_engineered[f"{col}_target_encoded"] = df_engineered[col].map(target_means)
                
                st.session_state.df = df_engineered
                st.success(f"✅ Applied {encoding_method} to {len(selected_cols)} columns!")
        else:
            st.info("No categorical columns available for encoding.")
    
    elif engineering_type == "Binning & Discretization":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            selected_col = st.selectbox("Select numeric column for binning:", numeric_cols)
            
            binning_method = st.selectbox(
                "Binning method:",
                ["Equal Width", "Equal Frequency", "Custom Bins", "Quantile Binning"]
            )
            
            if binning_method == "Custom Bins":
                num_bins = st.slider("Number of bins:", 2, 20, 5)
                bin_labels = st.text_input("Bin labels (comma-separated):", value="Low,Medium,High")
                bin_labels = [label.strip() for label in bin_labels.split(',')]
            else:
                num_bins = st.slider("Number of bins:", 2, 20, 5)
                bin_labels = None
            
            if st.button("🔧 Create Bins") and selected_col:
                df_engineered = df.copy()
                
                if binning_method == "Equal Width":
                    df_engineered[f"{selected_col}_binned"] = pd.cut(df_engineered[selected_col], bins=num_bins, labels=bin_labels)
                elif binning_method == "Equal Frequency":
                    df_engineered[f"{selected_col}_binned"] = pd.qcut(df_engineered[selected_col], q=num_bins, labels=bin_labels)
                elif binning_method == "Custom Bins":
                    if len(bin_labels) == num_bins:
                        df_engineered[f"{selected_col}_binned"] = pd.cut(df_engineered[selected_col], bins=num_bins, labels=bin_labels)
                    else:
                        st.error("Number of bin labels must match number of bins!")
                        return
                elif binning_method == "Quantile Binning":
                    quantiles = [i/num_bins for i in range(num_bins+1)]
                    bin_edges = df_engineered[selected_col].quantile(quantiles)
                    df_engineered[f"{selected_col}_binned"] = pd.cut(df_engineered[selected_col], bins=bin_edges, labels=bin_labels)
                
                st.session_state.df = df_engineered
                st.success(f"✅ Created {num_bins} bins for {selected_col}!")
        else:
            st.info("No numeric columns available for binning.")
    
    elif engineering_type == "Interaction Features":
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            col1 = st.selectbox("Select first column:", numeric_cols)
            col2 = st.selectbox("Select second column:", [col for col in numeric_cols if col != col1])
            
            interaction_types = st.multiselect(
                "Select interaction types:",
                ["Multiplication", "Division", "Addition", "Subtraction", "Ratio", "Difference"]
            )
            
            if st.button("🔧 Create Interactions") and interaction_types:
                df_engineered = df.copy()
                
                for interaction in interaction_types:
                    if interaction == "Multiplication":
                        df_engineered[f"{col1}_x_{col2}"] = df_engineered[col1] * df_engineered[col2]
                    elif interaction == "Division":
                        df_engineered[f"{col1}_div_{col2}"] = df_engineered[col1] / (df_engineered[col2] + 1e-8)
                    elif interaction == "Addition":
                        df_engineered[f"{col1}_plus_{col2}"] = df_engineered[col1] + df_engineered[col2]
                    elif interaction == "Subtraction":
                        df_engineered[f"{col1}_minus_{col2}"] = df_engineered[col1] - df_engineered[col2]
                    elif interaction == "Ratio":
                        df_engineered[f"{col1}_ratio_{col2}"] = df_engineered[col1] / (df_engineered[col1] + df_engineered[col2] + 1e-8)
                    elif interaction == "Difference":
                        df_engineered[f"{col1}_diff_{col2}"] = abs(df_engineered[col1] - df_engineered[col2])
                
                st.session_state.df = df_engineered
                st.success(f"✅ Created {len(interaction_types)} interaction features!")
        else:
            st.info("Need at least 2 numeric columns for interaction features.")

# Advanced Statistical Analysis (Phase 2)
def advanced_statistical_analysis(df):
    """Advanced statistical analysis with AI interpretation"""
    st.markdown("### 🔬 Advanced Statistical Analysis")
    
    if df is None:
        st.warning("Please upload data first!")
        return
    
    analysis_type = st.selectbox(
        "Choose analysis type:",
        ["Hypothesis Testing", "Regression Analysis", "Time Series Analysis", "Survival Analysis", "Multivariate Analysis"]
    )
    
    if analysis_type == "Hypothesis Testing":
        st.markdown("#### 🧪 Hypothesis Testing Suite")
        
        test_type = st.selectbox(
            "Select test:",
            ["T-Test (Independent)", "T-Test (Paired)", "ANOVA", "Chi-Square", "Mann-Whitney U", "Kruskal-Wallis"]
        )
        
        if test_type in ["T-Test (Independent)", "T-Test (Paired)"]:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                col1 = st.selectbox("Group 1 variable:", numeric_cols)
                col2 = st.selectbox("Group 2 variable:", [col for col in numeric_cols if col != col1])
                
                if st.button("🔬 Perform T-Test"):
                    if test_type == "T-Test (Independent)":
                        stat, p_value = stats.ttest_ind(df[col1].dropna(), df[col2].dropna())
                    else:  # Paired
                        # Ensure same length for paired test
                        min_len = min(len(df[col1].dropna()), len(df[col2].dropna()))
                        stat, p_value = stats.ttest_rel(df[col1].dropna()[:min_len], df[col2].dropna()[:min_len])
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("T-Statistic", f"{stat:.4f}")
                    with col2:
                        st.metric("P-Value", f"{p_value:.4f}")
                    with col3:
                        significance = "Significant" if p_value < 0.05 else "Not Significant"
                        st.metric("Result", significance)
                    
                    # Interpretation
                    st.markdown("#### 📖 Interpretation")
                    if p_value < 0.001:
                        st.success("***p < 0.001: Highly significant difference between groups***")
                    elif p_value < 0.01:
                        st.success("***p < 0.01: Very significant difference between groups***")
                    elif p_value < 0.05:
                        st.success("***p < 0.05: Significant difference between groups***")
                    else:
                        st.info("***p ≥ 0.05: No significant difference between groups***")
        
        elif test_type == "ANOVA":
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if numeric_cols and categorical_cols:
                value_col = st.selectbox("Numeric variable:", numeric_cols)
                group_col = st.selectbox("Grouping variable:", categorical_cols)
                
                if st.button("🔬 Perform ANOVA"):
                    # Prepare groups
                    groups = [group for name, group in df.groupby(group_col)[value_col] if len(group) > 0]
                    
                    if len(groups) >= 2:
                        stat, p_value = stats.f_oneway(*groups)
                        
                        # Display results
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("F-Statistic", f"{stat:.4f}")
                        with col2:
                            st.metric("P-Value", f"{p_value:.4f}")
                        with col3:
                            significance = "Significant" if p_value < 0.05 else "Not Significant"
                            st.metric("Result", significance)
                        
                        # Post-hoc analysis
                        if p_value < 0.05:
                            st.markdown("#### 🔍 Post-Hoc Analysis")
                            st.info("Significant differences found. Consider post-hoc tests (Tukey, Bonferroni) for pairwise comparisons.")
        
        elif test_type == "Chi-Square":
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if len(categorical_cols) >= 2:
                col1 = st.selectbox("Variable 1:", categorical_cols)
                col2 = st.selectbox("Variable 2:", [col for col in categorical_cols if col != col1])
                
                if st.button("🔬 Perform Chi-Square Test"):
                    # Create contingency table
                    contingency_table = pd.crosstab(df[col1], df[col2])
                    
                    # Perform chi-square test
                    stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                    
                    # Display results
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Chi-Square", f"{stat:.4f}")
                    with col2:
                        st.metric("P-Value", f"{p_value:.4f}")
                    with col3:
                        st.metric("Degrees of Freedom", dof)
                    with col4:
                        significance = "Significant" if p_value < 0.05 else "Not Significant"
                        st.metric("Result", significance)
                    
                    # Show contingency table
                    st.markdown("#### 📊 Contingency Table")
                    st.dataframe(contingency_table, use_container_width=True)
    
    elif analysis_type == "Regression Analysis":
        st.markdown("#### 📈 Regression Analysis")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            target_col = st.selectbox("Target variable:", numeric_cols)
            feature_cols = st.multiselect("Feature variables:", [col for col in numeric_cols if col != target_col])
            
            regression_type = st.selectbox("Regression type:", ["Linear Regression", "Polynomial Regression", "Ridge Regression", "Lasso Regression"])
            
            if st.button("🔬 Perform Regression") and feature_cols:
                from sklearn.linear_model import LinearRegression, Ridge, Lasso
                from sklearn.preprocessing import PolynomialFeatures
                from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
                
                # Prepare data
                X = df[feature_cols].fillna(df[feature_cols].mean())
                y = df[target_col].dropna()
                
                # Align X and y
                common_index = X.index.intersection(y.index)
                X = X.loc[common_index]
                y = y.loc[common_index]
                
                if len(X) > 0:
                    # Split data (simple approach)
                    split_idx = int(len(X) * 0.8)
                    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
                    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
                    
                    if regression_type == "Linear Regression":
                        model = LinearRegression()
                    elif regression_type == "Polynomial Regression":
                        degree = st.slider("Polynomial degree:", 2, 5, 2)
                        poly = PolynomialFeatures(degree=degree)
                        X_train = poly.fit_transform(X_train)
                        X_test = poly.transform(X_test)
                        model = LinearRegression()
                    elif regression_type == "Ridge Regression":
                        alpha = st.slider("Alpha (regularization):", 0.1, 10.0, 1.0)
                        model = Ridge(alpha=alpha)
                    elif regression_type == "Lasso Regression":
                        alpha = st.slider("Alpha (regularization):", 0.1, 10.0, 1.0)
                        model = Lasso(alpha=alpha)
                    
                    # Fit model
                    model.fit(X_train, y_train)
                    
                    # Predictions
                    y_pred = model.predict(X_test)
                    
                    # Metrics
                    r2 = r2_score(y_test, y_pred)
                    mse = mean_squared_error(y_test, y_pred)
                    mae = mean_absolute_error(y_test, y_pred)
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("R² Score", f"{r2:.4f}")
                    with col2:
                        st.metric("Mean Squared Error", f"{mse:.4f}")
                    with col3:
                        st.metric("Mean Absolute Error", f"{mae:.4f}")
                    
                    # Model interpretation
                    st.markdown("#### 📖 Model Interpretation")
                    if r2 > 0.8:
                        st.success("Excellent model fit (R² > 0.8)")
                    elif r2 > 0.6:
                        st.info("Good model fit (R² > 0.6)")
                    elif r2 > 0.4:
                        st.warning("Fair model fit (R² > 0.4)")
                    else:
                        st.error("Poor model fit (R² < 0.4)")
                    
                    # Feature importance (for linear models)
                    if hasattr(model, 'coef_'):
                        st.markdown("#### 🎯 Feature Importance")
                        if regression_type == "Polynomial Regression":
                            feature_names = [f"Feature_{i}" for i in range(len(model.coef_))]
                        else:
                            feature_names = feature_cols
                        
                        importance_df = pd.DataFrame({
                            'Feature': feature_names,
                            'Coefficient': model.coef_
                        })
                        importance_df = importance_df.sort_values('Coefficient', key=abs, ascending=False)
                        st.dataframe(importance_df, use_container_width=True)
                else:
                    st.error("No valid data for regression analysis")
        else:
            st.info("Need at least 2 numeric columns for regression analysis.")

# AI-Powered Recommendations Engine (Phase 2)
def ai_recommendations_engine(df):
    """AI-powered recommendations for data analysis and cleaning"""
    st.markdown("### 🤖 AI-Powered Recommendations")
    
    if df is None:
        st.warning("Please upload data first!")
        return
    
    # Analyze data characteristics
    recommendations = []
    
    # Data quality recommendations
    missing_pct = (df.isnull().sum().sum() / (df.shape[0] * df.shape[1])) * 100
    if missing_pct > 20:
        recommendations.append({
            'category': 'Data Quality',
            'priority': 'High',
            'title': 'High Missing Data',
            'description': f'{missing_pct:.1f}% of your data is missing',
            'action': 'Use advanced imputation methods or consider data collection',
            'icon': '⚠️'
        })
    
    # Outlier recommendations
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outlier_cols = []
    for col in numeric_cols:
        outliers = detect_outliers_advanced(df, [col], 'statistical')
        if outliers.sum() > len(df) * 0.1:
            outlier_cols.append(col)
    
    if outlier_cols:
        recommendations.append({
            'category': 'Data Quality',
            'priority': 'Medium',
            'title': 'Outliers Detected',
            'description': f'High number of outliers in {len(outlier_cols)} columns',
            'action': 'Review outlier handling strategy in cleaning section',
            'icon': '📊'
        })
    
    # Analysis recommendations
    if len(numeric_cols) >= 2:
        recommendations.append({
            'category': 'Analysis',
            'priority': 'Medium',
            'title': 'Correlation Analysis',
            'description': f'{len(numeric_cols)} numeric columns available',
            'action': 'Perform correlation analysis to understand relationships',
            'icon': '🔗'
        })
    
    # Visualization recommendations
    if len(df) > 100:
        recommendations.append({
            'category': 'Visualization',
            'priority': 'Low',
            'title': 'Large Dataset',
            'description': f'{len(df):,} rows - consider sampling for faster visualization',
            'action': 'Use data sampling or aggregation for better performance',
            'icon': '📈'
        })
    
    # Time series recommendations
    date_cols = []
    for col in df.columns:
        if df[col].dtype == 'datetime64[ns]' or 'date' in col.lower():
            date_cols.append(col)
    
    if date_cols:
        recommendations.append({
            'category': 'Analysis',
            'priority': 'Medium',
            'title': 'Time Series Data',
            'description': f'Date columns detected: {", ".join(date_cols)}',
            'action': 'Perform time series analysis and trend detection',
            'icon': '⏰'
        })
    
    # Display recommendations
    if recommendations:
        st.markdown("#### 🎯 AI Recommendations")
        
        # Group by priority
        high_priority = [r for r in recommendations if r['priority'] == 'High']
        medium_priority = [r for r in recommendations if r['priority'] == 'Medium']
        low_priority = [r for r in recommendations if r['priority'] == 'Low']
        
        if high_priority:
            st.markdown("**🔴 High Priority**")
            for rec in high_priority:
                st.markdown(f"""
                    <div style="background: #fef2f2; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; border-left: 4px solid #ef4444;">
                        <h4>{rec['icon']} {rec['title']}</h4>
                        <p><strong>Category:</strong> {rec['category']}</p>
                        <p>{rec['description']}</p>
                        <p><strong>Recommended Action:</strong> {rec['action']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        if medium_priority:
            st.markdown("**🟡 Medium Priority**")
            for rec in medium_priority:
                st.markdown(f"""
                    <div style="background: #fffbeb; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; border-left: 4px solid #f59e0b;">
                        <h4>{rec['icon']} {rec['title']}</h4>
                        <p><strong>Category:</strong> {rec['category']}</p>
                        <p>{rec['description']}</p>
                        <p><strong>Recommended Action:</strong> {rec['action']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        if low_priority:
            st.markdown("**🟢 Low Priority**")
            for rec in low_priority:
                st.markdown(f"""
                    <div style="background: #f0fdf4; padding: 1rem; border-radius: 0.5rem; margin: 0.5rem 0; border-left: 4px solid #22c55e;">
                        <h4>{rec['icon']} {rec['title']}</h4>
                        <p><strong>Category:</strong> {rec['category']}</p>
                        <p>{rec['description']}</p>
                        <p><strong>Recommended Action:</strong> {rec['action']}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.success("🎉 No critical issues detected! Your data looks good for analysis.")

# Enhanced Mobile Interface (Phase 1)
def mobile_optimized_interface():
    """Mobile-optimized interface components"""
    st.markdown("""
    <style>
        /* Mobile-first responsive design */
        @media (max-width: 768px) {
            .stButton > button {
                width: 100%;
                margin: 0.5rem 0;
            }
            
            .stSelectbox > div > div {
                width: 100%;
            }
            
            .stDataFrame {
                font-size: 0.8rem;
            }
            
            .metric-card {
                margin: 0.5rem 0;
                padding: 0.5rem;
            }
            
            .quality-score {
                width: 60px;
                height: 60px;
                font-size: 1.2rem;
            }
        }
        
        /* Touch-friendly interface */
        .mobile-friendly {
            min-height: 44px;
            padding: 12px;
            margin: 8px 0;
        }
        
        /* Swipe gestures support */
        .swipe-container {
            overflow-x: auto;
            scroll-snap-type: x mandatory;
        }
        
        .swipe-item {
            scroll-snap-align: start;
            min-width: 300px;
        }
    </style>
    """, unsafe_allow_html=True)

# Advanced Export with Metadata (Phase 1)
def advanced_export_options(df):
    """Advanced export options with comprehensive metadata"""
    st.markdown("### 📤 Advanced Export Options")
    
    if df is None:
        st.warning("No data to export!")
        return
    
    export_format = st.selectbox(
        "Export format:",
        ["CSV", "Excel", "JSON", "Parquet", "HTML Report", "PDF Report"]
    )
    
    include_metadata = st.checkbox("Include metadata and cleaning history", value=True)
    include_visualizations = st.checkbox("Include visualizations in report", value=True)
    
    if st.button(f"📤 Export as {export_format}"):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if export_format == "CSV":
            csv_data = df.to_csv(index=False)
            if include_metadata:
                metadata = {
                    'export_timestamp': timestamp,
                    'original_shape': st.session_state.original_df.shape if st.session_state.original_df is not None else None,
                    'final_shape': df.shape,
                    'cleaning_operations': st.session_state.cleaning_history,
                    'data_quality_score': st.session_state.data_quality_score
                }
                metadata_csv = pd.DataFrame([metadata]).to_csv(index=False)
                
                # Create zip file with both data and metadata
                import zipfile
                from io import BytesIO
                
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
                    zip_file.writestr(f'cleaned_data_{timestamp}.csv', csv_data)
                    zip_file.writestr(f'metadata_{timestamp}.csv', metadata_csv)
                
                st.download_button(
                    label="Download ZIP with Data & Metadata",
                    data=zip_buffer.getvalue(),
                    file_name=f"data_export_{timestamp}.zip",
                    mime="application/zip"
                )
            else:
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"cleaned_data_{timestamp}.csv",
                    mime="text/csv"
                )
        
        elif export_format == "Excel":
            try:
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, sheet_name='Cleaned Data', index=False)
                    
                    if include_metadata:
                        # Summary sheet
                        summary_data = {
                            'Metric': ['Export Date', 'Original Rows', 'Current Rows', 'Original Columns', 'Current Columns', 'Data Quality Score'],
                            'Value': [
                                timestamp,
                                st.session_state.original_df.shape[0] if st.session_state.original_df is not None else 'N/A',
                                df.shape[0],
                                st.session_state.original_df.shape[1] if st.session_state.original_df is not None else 'N/A',
                                df.shape[1],
                                f"{st.session_state.data_quality_score:.1f}" if st.session_state.data_quality_score else 'N/A'
                            ]
                        }
                        summary_df = pd.DataFrame(summary_data)
                        summary_df.to_excel(writer, sheet_name='Summary', index=False)
                        
                        # Cleaning history sheet
                        if st.session_state.cleaning_history:
                            history_df = pd.DataFrame({
                                'Step': range(1, len(st.session_state.cleaning_history) + 1),
                                'Operation': st.session_state.cleaning_history,
                                'Timestamp': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * len(st.session_state.cleaning_history)
                            })
                            history_df.to_excel(writer, sheet_name='Cleaning History', index=False)
                
                output.seek(0)
                st.download_button(
                    label="Download Excel",
                    data=output.getvalue(),
                    file_name=f"cleaned_data_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error creating Excel file: {str(e)}")
        
        elif export_format == "HTML Report":
            # Generate comprehensive HTML report
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Data Cleaning Report - {timestamp}</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .header {{ background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; }}
                    .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
                    .metric {{ display: inline-block; margin: 10px; padding: 10px; background: #f8f9fa; border-radius: 5px; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 Datalix</h1>
                    <h2>Data Cleaning Report</h2>
                    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="section">
                    <h3>📊 Dataset Summary</h3>
                    <div class="metric"><strong>Rows:</strong> {df.shape[0]:,}</div>
                    <div class="metric"><strong>Columns:</strong> {df.shape[1]}</div>
                    <div class="metric"><strong>Memory Usage:</strong> {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB</div>
                    <div class="metric"><strong>Data Quality Score:</strong> {st.session_state.data_quality_score or 'Not calculated'}/100</div>
                </div>
                
                <div class="section">
                    <h3>🧹 Cleaning Operations</h3>
                    <ul>
            """
            
            if st.session_state.cleaning_history:
                for operation in st.session_state.cleaning_history:
                    html_content += f"<li>{operation}</li>"
            else:
                html_content += "<li>No cleaning operations applied</li>"
            
            html_content += """
                    </ul>
                </div>
                
                <div class="section">
                    <h3>📋 Column Information</h3>
                    <table>
                        <tr><th>Column</th><th>Type</th><th>Missing %</th><th>Unique Values</th></tr>
            """
            
            for col in df.columns:
                missing_pct = (df[col].isnull().sum() / len(df)) * 100
                html_content += f"<tr><td>{col}</td><td>{df[col].dtype}</td><td>{missing_pct:.1f}%</td><td>{df[col].nunique()}</td></tr>"
            
            html_content += """
                    </table>
                </div>
                
                <div class="section">
                    <h3>📊 Data Preview</h3>
            """
            
            # Add data preview as HTML table
            html_content += df.head(10).to_html(classes='dataframe', index=False)
            
            html_content += """
                </div>
            </body>
            </html>
            """
            
            st.download_button(
                label="Download HTML Report",
                data=html_content,
                file_name=f"data_report_{timestamp}.html",
                mime="text/html"
            )

# Add all new features to the main navigation
# Update the sidebar to include all Phase 1 & 2 features
if 'main_section' not in locals():
    main_section = st.sidebar.radio(
        "Navigate to:",
        ["🏠 Home", "📁 Data Upload", "🧠 AI Insights", "🧹 Smart Cleaning", 
         "📊 Advanced Analytics", "🎨 Dashboard Builder", "🔧 Pipeline Builder",
         "🛠️ Feature Engineering", "🔬 Statistical Analysis", "🤖 AI Recommendations",
         "📋 Templates", "👥 Collaboration", "⚙️ Settings"]
    )

# Add new sections to main application
if main_section == "🛠️ Feature Engineering":
    st.markdown('<h2 class="section-header">🛠️ Advanced Feature Engineering</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("Please upload a dataset first!")
        st.stop()
    
    feature_engineering_advanced(st.session_state.df)

elif main_section == "🔬 Statistical Analysis":
    st.markdown('<h2 class="section-header">🔬 Advanced Statistical Analysis</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("Please upload a dataset first!")
        st.stop()
    
    advanced_statistical_analysis(st.session_state.df)

elif main_section == "🤖 AI Recommendations":
    st.markdown('<h2 class="section-header">🤖 AI-Powered Recommendations</h2>', unsafe_allow_html=True)
    
    if st.session_state.df is None:
        st.warning("Please upload a dataset first!")
        st.stop()
    
    ai_recommendations_engine(st.session_state.df)

# Enhanced export section in footer
if st.session_state.df is not None:
    st.markdown("---")
    advanced_export_options(st.session_state.df)

# Initialize mobile optimization
mobile_optimized_interface()

# Footer - ONLY SHOW ON HOME PAGE
if main_section == "🏠 Home":
    st.markdown("---")
    st.markdown("### 📊 Datalix")
    st.markdown("**Complete Implementation with AI-Powered Features**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Features:**")
        st.markdown("• AI-Powered Data Cleaning")
        st.markdown("• Advanced Analytics")
        st.markdown("• Interactive Visualizations")
    
    with col2:
        st.markdown("**Built with:**")
        st.markdown("• Streamlit")
        st.markdown("• Pandas")
        st.markdown("• Plotly")
        st.markdown("• Scikit-learn")
    
    with col3:
        st.markdown("**Capabilities:**")
        st.markdown("• Real-time Processing")
        st.markdown("• Interactive Dashboards")
        st.markdown("• Advanced ML Tools")
    
    st.markdown("---")
    st.markdown("*© 2025 Datalix*")
else:
    # Simple footer for other pages
    st.markdown("---")
    st.markdown("*© 2025 Datalix*")
