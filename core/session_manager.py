"""
Session state management
"""

import streamlit as st
from typing import Any, Optional


class SessionManager:
    """Manage Streamlit session state"""
    
    def __init__(self):
        self.initialize_state()
    
    def initialize_state(self):
        """Initialize session state variables"""
        defaults = {
            'data': None,
            'original_data': None,
            'file_info': {},
            'quality_score': None,
            'current_page': 'Home'
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from session state"""
        return st.session_state.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set value in session state"""
        st.session_state[key] = value
    
    def clear(self):
        """Clear all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        self.initialize_state()
