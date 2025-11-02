"""Database operations using DuckDB"""
import logging
from typing import Any

import duckdb

logger = logging.getLogger(__name__)


class Database:
    """DuckDB database handler"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = duckdb.connect(db_path)
    
    def close(self) -> None:
        """Close database connection"""
        self.conn.close()
    
    def load_data(self, file_path: str) -> int:
        """Load pipe-separated employee data into main_data table"""
        logger.info(f"Loading data from {file_path}...")
        
        # Load pipe-separated file into main_data table
        self.conn.execute("""
            CREATE OR REPLACE TABLE main_data AS 
            SELECT 
                row_number() OVER () as row_id,
                column0 as emp_id,
                column1 as emp_name,
                column2 as emp_type,
                column3 as dept,
                column4 as expected_grade
            FROM read_csv(?, delim='|', header=true, columns={
                'column0': 'VARCHAR',
                'column1': 'VARCHAR', 
                'column2': 'VARCHAR',
                'column3': 'VARCHAR',
                'column4': 'VARCHAR'
            })
        """, [file_path])
        
        # Create control table with results columns
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS process_control (
                row_id INTEGER PRIMARY KEY,
                status TEXT DEFAULT 'pending',
                valuation_index FLOAT,
                calculated_grade VARCHAR,
                expected_grade VARCHAR,
                validation_status VARCHAR,
                last_error TEXT,
                attempts INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Initialize control records
        self.conn.execute("""
            INSERT INTO process_control (row_id, status, expected_grade)
            SELECT row_id, 'pending', expected_grade 
            FROM main_data
            ON CONFLICT (row_id) DO NOTHING
        """)
        
        total = self.conn.execute("SELECT COUNT(*) FROM main_data").fetchone()[0]
        logger.info(f"✓ Loaded {total} records")
        return total
    
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
        
        query = f"""
            SELECT 
                main_data.row_id,
                main_data.emp_id,
                main_data.emp_name,
                main_data.emp_type,
                main_data.dept,
                main_data.expected_grade
            FROM main_data
            INNER JOIN process_control ON main_data.row_id = process_control.row_id
            WHERE {where_clause}
            ORDER BY main_data.row_id
        """
        
        return self.conn.execute(query, params).fetchall()
    
    def update_success_with_results(
        self,
        row_id: int,
        valuation_index: float,
        calculated_grade: str,
        expected_grade: str,
        validation_status: str
    ) -> None:
        """Mark row as successfully processed with results"""
        self.conn.execute("""
            UPDATE process_control 
            SET 
                status='success',
                valuation_index=?,
                calculated_grade=?,
                expected_grade=?,
                validation_status=?,
                last_error=NULL,
                updated_at=CURRENT_TIMESTAMP
            WHERE row_id=?
        """, [valuation_index, calculated_grade, expected_grade, validation_status, row_id])
    
    def update_failure(self, row_id: int, error_msg: str) -> None:
        """Mark row as failed"""
        error_msg = str(error_msg)[:500]
        self.conn.execute("""
            UPDATE process_control 
            SET status='failed', last_error=?, attempts=attempts+1, updated_at=CURRENT_TIMESTAMP
            WHERE row_id=?
        """, [error_msg, row_id])
    
    def get_validation_summary(self) -> list[tuple]:
        """Get validation summary (PASS/FAIL counts)"""
        return self.conn.execute("""
            SELECT 
                validation_status,
                COUNT(*) as count,
                ROUND(AVG(valuation_index), 2) as avg_index
            FROM process_control
            WHERE status = 'success'
            GROUP BY validation_status
            ORDER BY validation_status
        """).fetchall()
    
    def get_grade_distribution(self) -> list[tuple]:
        """Get calculated grade distribution"""
        return self.conn.execute("""
            SELECT 
                calculated_grade,
                COUNT(*) as count
            FROM process_control
            WHERE status = 'success'
            GROUP BY calculated_grade
            ORDER BY calculated_grade
        """).fetchall()
    
    def get_mismatches(self) -> list[tuple]:
        """Get records where calculated grade != expected grade"""
        return self.conn.execute("""
            SELECT 
                main_data.emp_id,
                main_data.emp_name,
                process_control.valuation_index,
                process_control.calculated_grade,
                process_control.expected_grade
            FROM main_data
            INNER JOIN process_control ON main_data.row_id = process_control.row_id
            WHERE process_control.validation_status = 'FAIL'
            ORDER BY main_data.row_id
        """).fetchall()
    
    def get_status_summary(self, start: int | None = None, end: int | None = None) -> list[tuple]:
        """Get status summary with optional range filter"""
        where_parts = []
        if start is not None and end is not None:
            where_parts.append(f"row_id BETWEEN {start} AND {end}")
        elif start is not None:
            where_parts.append(f"row_id >= {start}")
        elif end is not None:
            where_parts.append(f"row_id <= {end}")
        
        where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
        
        return self.conn.execute(f"""
            SELECT status, COUNT(*) as count
            FROM process_control
            {where_clause}
            GROUP BY status
            ORDER BY status
        """).fetchall()
    
    def get_total_count(self, start: int | None = None, end: int | None = None) -> int:
        """Get total record count with optional range filter"""
        where_parts = []
        if start is not None and end is not None:
            where_parts.append(f"row_id BETWEEN {start} AND {end}")
        elif start is not None:
            where_parts.append(f"row_id >= {start}")
        elif end is not None:
            where_parts.append(f"row_id <= {end}")
        
        where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
        
        return self.conn.execute(f"SELECT COUNT(*) FROM process_control {where_clause}").fetchone()[0]
    
    def get_failure_count(self) -> int:
        """Get total number of failed records"""
        return self.conn.execute("SELECT COUNT(*) FROM process_control WHERE status='failed'").fetchone()[0]
    
    def reset_failed(self) -> None:
        """Reset failed records to pending"""
        self.conn.execute("UPDATE process_control SET status='pending' WHERE status='failed'")
    
    def reset_range(self, start: int | None = None, end: int | None = None) -> None:
        """Reset records to pending within optional range"""
        if start is not None and end is not None:
            self.conn.execute(
                "UPDATE process_control SET status='pending', last_error=NULL, attempts=0 WHERE row_id BETWEEN ? AND ?",
                [start, end]
            )
        elif start is not None:
            self.conn.execute(
                "UPDATE process_control SET status='pending', last_error=NULL, attempts=0 WHERE row_id >= ?",
                [start]
            )
        elif end is not None:
            self.conn.execute(
                "UPDATE process_control SET status='pending', last_error=NULL, attempts=0 WHERE row_id <= ?",
                [end]
            )
        else:
            self.conn.execute("UPDATE process_control SET status='pending', last_error=NULL, attempts=0")
