"""
Database Connector Module
Handles PostgreSQL and MySQL connections for data import/export
"""

import pandas as pd
from sqlalchemy import create_engine, text, inspect
from typing import Optional, List, Dict, Tuple, Literal
import streamlit as st


class DatabaseConnector:
    """Handle database connections and operations"""
    
    def __init__(self):
        self.engine = None
        self.connection_params = {}
        self.db_type = None
    
    def connect(self, db_type: str, host: str, port: int, 
                database: str, username: str, password: str) -> Tuple[bool, str]:
        """
        Connect to a database
        
        Args:
            db_type: 'postgresql' or 'mysql'
            host: Database host
            port: Database port
            database: Database name
            username: Username
            password: Password
        
        Returns:
            Tuple[bool, str]: Success status and message
        """
        try:
            if db_type == 'postgresql':
                connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
            elif db_type == 'mysql':
                connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            else:
                return False, f"Unsupported database type: {db_type}"
            
            self.engine = create_engine(connection_string)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.connection_params = {
                'db_type': db_type,
                'host': host,
                'port': port,
                'database': database,
                'username': username
            }
            self.db_type = db_type
            
            return True, f"Successfully connected to {db_type} database: {database}"
        
        except Exception as e:
            self.engine = None
            return False, f"Connection failed: {str(e)}"
    
    def disconnect(self):
        """Disconnect from database"""
        if self.engine:
            self.engine.dispose()
            self.engine = None
            self.connection_params = {}
            self.db_type = None
    
    def is_connected(self) -> bool:
        """Check if connected to database"""
        return self.engine is not None
    
    def list_tables(self) -> List[str]:
        """
        List all tables in the database
        
        Returns:
            List[str]: List of table names
        """
        if not self.is_connected():
            return []
        
        try:
            assert self.engine is not None
            inspector = inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            st.error(f"Error listing tables: {str(e)}")
            return []
    
    def get_table_info(self, table_name: str) -> Dict:
        """
        Get information about a table
        
        Args:
            table_name: Name of the table
        
        Returns:
            Dict: Table information
        """
        if not self.is_connected():
            return {}
        
        try:
            assert self.engine is not None
            inspector = inspect(self.engine)
            columns = inspector.get_columns(table_name)
            
            return {
                'columns': [col['name'] for col in columns],
                'column_types': {col['name']: str(col['type']) for col in columns},
                'total_columns': len(columns)
            }
        except Exception as e:
            st.error(f"Error getting table info: {str(e)}")
            return {}
    
    def import_table(self, table_name: str, limit: Optional[int] = None,
                    query: Optional[str] = None) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Import data from a database table
        
        Args:
            table_name: Name of the table
            limit: Maximum number of rows to import
            query: Optional custom SQL query
        
        Returns:
            Tuple[Optional[pd.DataFrame], str]: DataFrame and message
        """
        if not self.is_connected():
            return None, "Not connected to database"
        
        try:
            if query:
                sql = query
            else:
                sql = f"SELECT * FROM {table_name}"
                if limit:
                    if self.db_type == 'postgresql':
                        sql += f" LIMIT {limit}"
                    elif self.db_type == 'mysql':
                        sql += f" LIMIT {limit}"
            
            df = pd.read_sql(sql, self.engine)
            
            message = f"Successfully imported {len(df)} rows from {table_name}"
            if limit and len(df) >= limit:
                message += f" (limited to {limit} rows)"
            
            return df, message
        
        except Exception as e:
            return None, f"Error importing data: {str(e)}"
    
    def export_table(self, df: pd.DataFrame, table_name: str, 
                    if_exists: Literal['replace', 'append', 'fail'] = 'replace') -> Tuple[bool, str]:
        """
        Export DataFrame to database table
        
        Args:
            df: DataFrame to export
            table_name: Name of the table
            if_exists: 'replace', 'append', or 'fail'
        
        Returns:
            Tuple[bool, str]: Success status and message
        """
        if not self.is_connected():
            return False, "Not connected to database"
        
        try:
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=False)
            
            message = f"Successfully exported {len(df)} rows to table '{table_name}'"
            if if_exists == 'append':
                message += " (appended to existing table)"
            elif if_exists == 'replace':
                message += " (replaced existing table)"
            
            return True, message
        
        except Exception as e:
            return False, f"Error exporting data: {str(e)}"
    
    def execute_query(self, query: str) -> Tuple[Optional[pd.DataFrame], str]:
        """
        Execute a custom SQL query
        
        Args:
            query: SQL query to execute
        
        Returns:
            Tuple[Optional[pd.DataFrame], str]: Result DataFrame and message
        """
        if not self.is_connected():
            return None, "Not connected to database"
        
        try:
            # Check if query is SELECT
            if query.strip().upper().startswith('SELECT'):
                df = pd.read_sql(query, self.engine)
                return df, f"Query executed successfully. Retrieved {len(df)} rows."
            else:
                # For non-SELECT queries
                assert self.engine is not None
                with self.engine.connect() as conn:
                    result = conn.execute(text(query))
                    conn.commit()
                return None, f"Query executed successfully. Rows affected: {result.rowcount}"
        
        except Exception as e:
            return None, f"Error executing query: {str(e)}"
    
    def get_connection_info(self) -> Dict:
        """Get current connection information"""
        return self.connection_params.copy()
