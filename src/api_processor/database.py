"""Database operations using DuckDB"""
import logging
from typing import Any

import duckdb

from .config import Config
from .performance_decorators import measure_performance

logger = logging.getLogger(__name__)


class Database:
    """DuckDB database handler"""
    
    def __init__(self, config: Config):
        self.config = config
        self.db_path = config.db_path
        self.conn = duckdb.connect(self.db_path)
        self.sql = config.sql_queries
    
    def close(self) -> None:
        """Close database connection"""
        self.conn.close()
    
    @measure_performance(include_memory=True, threshold_ms=50.0, log_level=logging.INFO)
    def load_data(self, file_path: str) -> int:
        """Load pipe-separated employee data into main_data table"""
        logger.info(f"Loading data from {file_path}...")
        
        # Load pipe-separated file into main_data table
        self.conn.execute(self.sql["create_main_data_table"], [file_path])
        
        # Create control table with results columns
        self.conn.execute(self.sql["create_control_table"])
        
        # Initialize control records
        self.conn.execute(self.sql["initialize_control_records"])
        
        total = self.conn.execute(self.sql["count_main_data"]).fetchone()[0]
        logger.info(f"✓ Loaded {total} records")
        return total
    
    @measure_performance(include_memory=True, threshold_ms=20.0)
    def get_pending_rows(self, start: int | None = None, end: int | None = None) -> list[tuple]:
        """Get pending rows within optional range"""
        conditions = ["process_control.status = 'pending'"]
        params = []
        
        if start is not None and end is not None:
            conditions.append("main_data.row_id BETWEEN ? AND ?")
            params.extend([start, end])
        elif start is not None:
            conditions.append("main_data.row_id >= ?")
            params.append(start)
        elif end is not None:
            conditions.append("main_data.row_id <= ?")
            params.append(end)
        
        where_clause = " AND ".join(conditions)
        
        query = self.sql["get_pending_rows"].replace(
            "WHERE process_control.status = 'pending'",
            f"WHERE {where_clause}"
        )
        
        return self.conn.execute(query, params).fetchall()
    
    @measure_performance(include_memory=False, threshold_ms=5.0)
    def update_success_with_results(
        self,
        row_id: int,
        valuation_index: float,
        calculated_grade: str,
        expected_grade: str,
        validation_status: str
    ) -> None:
        """Mark row as successfully processed with results"""
        self.conn.execute(
            self.sql["update_success_with_results"],
            [valuation_index, calculated_grade, expected_grade, validation_status, row_id]
        )
    
    @measure_performance(include_memory=False, threshold_ms=5.0)
    def update_failure(self, row_id: int, error_msg: str) -> None:
        """Mark row as failed"""
        error_msg = str(error_msg)[:500]
        self.conn.execute(self.sql["update_failure"], [error_msg, row_id])
    
    def get_validation_summary(self) -> list[tuple]:
        """Get validation summary (PASS/FAIL counts)"""
        return self.conn.execute(self.sql["validation_summary"]).fetchall()
    
    def get_grade_distribution(self) -> list[tuple]:
        """Get calculated grade distribution"""
        return self.conn.execute(self.sql["grade_distribution"]).fetchall()
    
    def get_mismatches(self) -> list[tuple]:
        """Get records where calculated grade != expected grade"""
        return self.conn.execute(self.sql["mismatches"]).fetchall()
    
    @measure_performance(include_memory=True, threshold_ms=0.0, log_level=logging.INFO)
    def get_status_summary(self, start: int | None = None, end: int | None = None) -> list[tuple]:
        """Get status summary with optional range filter"""
        conditions = []
        params = []
        
        if start is not None and end is not None:
            conditions.append("row_id BETWEEN ? AND ?")
            params.extend([start, end])
        elif start is not None:
            conditions.append("row_id >= ?")
            params.append(start)
        elif end is not None:
            conditions.append("row_id <= ?")
            params.append(end)
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        query = self.sql["status_summary"].format(where_clause=where_clause)
        
        return self.conn.execute(query, params).fetchall()
    
    def get_total_count(self, start: int | None = None, end: int | None = None) -> int:
        """Get total record count with optional range filter"""
        conditions = []
        params = []
        
        if start is not None and end is not None:
            conditions.append("row_id BETWEEN ? AND ?")
            params.extend([start, end])
        elif start is not None:
            conditions.append("row_id >= ?")
            params.append(start)
        elif end is not None:
            conditions.append("row_id <= ?")
            params.append(end)
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        query = self.sql["total_count"].format(where_clause=where_clause)
        return self.conn.execute(query, params).fetchone()[0]
    
    def get_failure_count(self) -> int:
        """Get total number of failed records"""
        return self.conn.execute(self.sql["failure_count"]).fetchone()[0]
    
    def get_total_count(self, start: int | None = None, end: int | None = None) -> int:
        """Get total record count with optional range filter"""
        conditions = []
        params = []
        
        if start is not None and end is not None:
            conditions.append("row_id BETWEEN ? AND ?")
            params.extend([start, end])
        elif start is not None:
            conditions.append("row_id >= ?")
            params.append(start)
        elif end is not None:
            conditions.append("row_id <= ?")
            params.append(end)
        
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        query = f"SELECT COUNT(*) FROM process_control {where_clause}"
        return self.conn.execute(query, params).fetchone()[0]
    
    def get_failure_count(self) -> int:
        """Get total number of failed records"""
        return self.conn.execute("SELECT COUNT(*) FROM process_control WHERE status='failed'").fetchone()[0]
    
    def reset_failed(self) -> None:
        """Reset failed records to pending"""
        self.conn.execute(self.sql["reset_failed"])
    
    def reset_range(self, start: int | None = None, end: int | None = None) -> None:
        """Reset records to pending within optional range"""
        base_query = self.sql["reset_range"]
        
        if start is not None and end is not None:
            query = f"{base_query} WHERE row_id BETWEEN ? AND ?"
            self.conn.execute(query, [start, end])
        elif start is not None:
            query = f"{base_query} WHERE row_id >= ?"
            self.conn.execute(query, [start])
        elif end is not None:
            query = f"{base_query} WHERE row_id <= ?"
            self.conn.execute(query, [end])
        else:
            self.conn.execute(base_query)
