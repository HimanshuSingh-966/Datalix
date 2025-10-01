"""
File encoding detection utilities
"""

import chardet
from typing import Optional


class EncodingDetector:
    """Detect file encoding automatically"""
    
    def __init__(self):
        self.common_encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'windows-1252', 'ascii']
    
    def detect_encoding(self, uploaded_file, sample_size: int = 10000) -> str:
        """
        Detect the encoding of an uploaded file
        
        Args:
            uploaded_file: Streamlit uploaded file object
            sample_size: Number of bytes to sample for detection
        
        Returns:
            str: Detected encoding name
        """
        # Read sample
        uploaded_file.seek(0)
        sample = uploaded_file.read(sample_size)
        uploaded_file.seek(0)
        
        # Detect encoding
        result = chardet.detect(sample)
        detected_encoding = result['encoding']
        confidence = result['confidence']
        
        # If confidence is low, try common encodings
        if confidence < 0.7:
            for encoding in self.common_encodings:
                try:
                    sample.decode(encoding)
                    return encoding
                except:
                    continue
        
        # Return detected encoding or default to utf-8
        return detected_encoding if detected_encoding else 'utf-8'
    
    def validate_encoding(self, file_content: bytes, encoding: str) -> bool:
        """
        Validate if content can be decoded with given encoding
        
        Args:
            file_content: File content as bytes
            encoding: Encoding to validate
        
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            file_content.decode(encoding)
            return True
        except:
            return False
