"""Performance measurement decorators for timing and memory profiling

Units Used:
- Time: Stored in seconds (float), displayed as milliseconds (ms) for individual timings 
        and seconds (s) for totals
- Memory: Measured and displayed in megabytes (MB) using RSS memory and tracemalloc peak
- Storage: All metrics persisted in DuckDB database (db.duckdb)
"""
import asyncio
import functools
import logging
import os
import time
import tracemalloc
from pathlib import Path
from typing import Any, Callable, Dict, Optional
import psutil
import duckdb
from rich.console import Console
from rich.table import Table
from .emoji_support import emoji_handler

logger = logging.getLogger(__name__)

# DuckDB database file
DB_FILE = Path("db.duckdb")
console = Console()


class PerformanceMetrics:
    """Centralized performance metrics collection with DuckDB persistence"""
    
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}
        self.process = psutil.Process(os.getpid())
        self.conn = None
        self.init_database()
        self.load_metrics()
    
    def init_database(self):
        """Initialize DuckDB connection and create performance metrics table"""
        try:
            self.conn = duckdb.connect(str(DB_FILE))
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    function_name VARCHAR PRIMARY KEY,
                    calls INTEGER,
                    total_time DOUBLE,      -- seconds
                    min_time DOUBLE,        -- seconds  
                    max_time DOUBLE,        -- seconds
                    avg_time DOUBLE,        -- seconds
                    total_memory DOUBLE,    -- megabytes (MB)
                    avg_memory DOUBLE,      -- megabytes (MB) 
                    peak_memory DOUBLE,     -- megabytes (MB)
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        except Exception as e:
            logger.debug(f"Could not initialize performance metrics database: {e}")
    
    def load_metrics(self):
        """Load existing metrics from DuckDB"""
        try:
            if self.conn:
                result = self.conn.execute("""
                    SELECT function_name, calls, total_time, min_time, max_time, 
                           avg_time, total_memory, avg_memory, peak_memory
                    FROM performance_metrics
                """).fetchall()
                
                for row in result:
                    func_name, calls, total_time, min_time, max_time, avg_time, total_memory, avg_memory, peak_memory = row
                    self.metrics[func_name] = {
                        'calls': calls,
                        'total_time': total_time,
                        'min_time': min_time,
                        'max_time': max_time,
                        'avg_time': avg_time,
                        'total_memory': total_memory,
                        'avg_memory': avg_memory,
                        'peak_memory': peak_memory
                    }
        except Exception as e:
            logger.debug(f"Could not load performance metrics: {e}")
    
    def save_metrics(self):
        """Save current metrics to DuckDB"""
        try:
            if self.conn:
                # Use simpler INSERT OR REPLACE for DuckDB compatibility
                for func_name, metrics in self.metrics.items():
                    self.conn.execute("""
                        INSERT OR REPLACE INTO performance_metrics 
                        (function_name, calls, total_time, min_time, max_time, avg_time, 
                         total_memory, avg_memory, peak_memory)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, [
                        func_name, metrics['calls'], metrics['total_time'], 
                        metrics['min_time'], metrics['max_time'], metrics['avg_time'],
                        metrics['total_memory'], metrics['avg_memory'], metrics['peak_memory']
                    ])
        except Exception as e:
            logger.debug(f"Could not save performance metrics: {e}")
    
    def record_metric(self, func_name: str, duration: float, memory_delta: float, memory_peak: float):
        """Record performance metrics for a function
        
        Args:
            func_name: Name of the function
            duration: Execution time in seconds
            memory_delta: Memory change in MB (can be negative)
            memory_peak: Peak memory usage in MB for this call
        """
        if func_name not in self.metrics:
            self.metrics[func_name] = {
                'calls': 0,
                'total_time': 0.0,
                'avg_time': 0.0,
                'min_time': float('inf'),
                'max_time': 0.0,
                'total_memory': 0.0,
                'avg_memory': 0.0,
                'peak_memory': 0.0
            }
        
        metrics = self.metrics[func_name]
        metrics['calls'] += 1
        metrics['total_time'] += duration
        metrics['avg_time'] = metrics['total_time'] / metrics['calls']
        metrics['min_time'] = min(metrics['min_time'], duration)
        metrics['max_time'] = max(metrics['max_time'], duration)
        metrics['total_memory'] += memory_delta
        metrics['avg_memory'] = metrics['total_memory'] / metrics['calls']
        # Use the actual memory usage during the call, not cumulative max
        metrics['peak_memory'] = max(metrics['peak_memory'], memory_peak) if memory_peak > 0 else metrics['peak_memory']
        
        # Save after each update for persistence
        self.save_metrics()
    
    def get_performance_summary(self, memory_unit: str = "mb", time_unit: str = "auto") -> tuple:
        """Generate comprehensive performance summary using Rich formatting
        Returns tuple of (main_table, summary_table, slowest_table, title_messages)
        
        Args:
            memory_unit: Unit for memory display (bytes, kb, mb, gb)
            time_unit: Unit for time display (ns, us, ms, s, auto)
        """
        if not self.metrics:
            return None, None, None, [emoji_handler.format_message("info", "[yellow]No performance metrics available[/yellow]")]
        
        # Get unit labels for column headers
        _, memory_label = _format_memory(1.0, memory_unit)
        sample_time = 0.001  # 1ms sample for auto unit detection
        _, time_label = _format_time(sample_time, time_unit)
        
        # Create Rich table with dynamic column headers
        table = Table(show_header=True, header_style="bold magenta", title=emoji_handler.format_message("performance", "Performance Metrics Report"))
        table.add_column("Function", style="cyan", no_wrap=False, min_width=20)
        table.add_column("Calls", justify="right", style="green")
        table.add_column(f"Avg Time ({time_label})", justify="right", style="yellow")
        table.add_column(f"Min Time ({time_label})", justify="right", style="blue")
        table.add_column(f"Max Time ({time_label})", justify="right", style="blue")
        table.add_column("Total Time (s)", justify="right", style="red")  # Always show total in seconds
        table.add_column(f"Avg Mem ({memory_label})", justify="right", style="cyan")
        table.add_column(f"Peak Mem ({memory_label})", justify="right", style="magenta")
        
        # Sort by total time descending
        sorted_metrics = sorted(self.metrics.items(), key=lambda x: x[1]['total_time'], reverse=True)
        
        for func_name, metrics in sorted_metrics:
            # Format times
            avg_time_val, _ = _format_time(metrics['avg_time'], time_unit)
            min_time_val, _ = _format_time(metrics['min_time'], time_unit)
            max_time_val, _ = _format_time(metrics['max_time'], time_unit)
            
            # Format memory
            avg_memory_val, _ = _format_memory(metrics['avg_memory'], memory_unit)
            peak_memory_val, _ = _format_memory(metrics['peak_memory'], memory_unit)
            
            table.add_row(
                func_name,
                str(metrics['calls']),
                avg_time_val,
                min_time_val,
                max_time_val,
                f"{metrics['total_time']:.3f}",  # Always show total time in seconds
                avg_memory_val,
                peak_memory_val
            )
        
        # Calculate summary statistics
        total_calls = sum(m['calls'] for m in self.metrics.values())
        total_time = sum(m['total_time'] for m in self.metrics.values())
        avg_memory_across_all = sum(m['avg_memory'] * m['calls'] for m in self.metrics.values()) / total_calls if total_calls > 0 else 0
        peak_memory_overall = max(m['peak_memory'] for m in self.metrics.values()) if self.metrics else 0
        
        # Create summary section
        summary_table = Table(show_header=False, box=None, padding=(0, 1))
        summary_table.add_column("Metric", style="cyan", no_wrap=True)
        summary_table.add_column("Value", style="yellow", justify="left")
        
        summary_table.add_row("• Total Function Calls:", f"{total_calls:,}")
        summary_table.add_row("• Total Execution Time:", f"{total_time:.3f}s")
        summary_table.add_row("• Average Memory Usage:", f"{avg_memory_across_all:.2f} MB")
        summary_table.add_row("• Peak Memory Usage:", f"{peak_memory_overall:.2f} MB")
        
        # Create top slowest functions section
        slowest_table = Table(show_header=False, box=None, padding=(0, 1))
        slowest_table.add_column("Rank", style="white", no_wrap=True)
        slowest_table.add_column("Function", style="cyan")
        slowest_table.add_column("Time", style="red")
        
        slowest = sorted(self.metrics.items(), key=lambda x: x[1]['total_time'], reverse=True)[:3]
        for i, (func_name, metrics) in enumerate(slowest, 1):
            # Function names are already short (filename.function_name), so use them directly
            time_style = "red" if metrics['total_time'] > 0.1 else "yellow" if metrics['total_time'] > 0.01 else "green"
            slowest_table.add_row(
                f"{i}.",
                func_name,
                f"[{time_style}]{metrics['total_time']*1000:.1f}ms[/{time_style}] total ({metrics['calls']} calls)"
            )
        
        # Return Rich objects and title messages
        title_messages = [
            emoji_handler.format_message('info', 'Performance Summary Statistics'),
            emoji_handler.format_message('info', 'Top 3 Slowest Functions (by total time)')
        ]
        
        return table, summary_table, slowest_table, title_messages
    
    def clear_metrics(self):
        """Clear all metrics from memory and database"""
        self.metrics.clear()
        try:
            if self.conn:
                self.conn.execute("DELETE FROM performance_metrics")
        except Exception as e:
            logger.debug(f"Could not clear performance metrics: {e}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            self.conn = None


# Global metrics instance
performance_metrics = PerformanceMetrics()


def _format_func_name(func) -> str:
    """Format function name to show only filename.function_name"""
    module_parts = func.__module__.split('.')
    filename = module_parts[-1] if module_parts else 'unknown'
    return f"{filename}.{func.__qualname__}"


def _format_memory(value_mb: float, unit: str) -> tuple[str, str]:
    """Convert memory from MB to the specified unit and return (value, unit_label)"""
    if unit == "bytes":
        return f"{value_mb * 1024 * 1024:.0f}", "B"
    elif unit == "kb":
        return f"{value_mb * 1024:.2f}", "KB"
    elif unit == "mb":
        return f"{value_mb:.2f}", "MB"
    elif unit == "gb":
        return f"{value_mb / 1024:.3f}", "GB"
    else:
        return f"{value_mb:.2f}", "MB"  # Default to MB


def _format_time(value_seconds: float, unit: str) -> tuple[str, str]:
    """Convert time from seconds to the specified unit and return (value, unit_label)"""
    if unit == "auto":
        # Auto-select appropriate unit based on magnitude
        if value_seconds >= 1.0:
            return f"{value_seconds:.3f}", "s"
        elif value_seconds >= 0.001:
            return f"{value_seconds * 1000:.2f}", "ms"
        elif value_seconds >= 0.000001:
            return f"{value_seconds * 1000000:.1f}", "μs"
        else:
            return f"{value_seconds * 1000000000:.0f}", "ns"
    elif unit == "ns":
        return f"{value_seconds * 1000000000:.0f}", "ns"
    elif unit == "us":
        return f"{value_seconds * 1000000:.1f}", "μs"
    elif unit == "ms":
        return f"{value_seconds * 1000:.2f}", "ms"
    elif unit == "s":
        return f"{value_seconds:.3f}", "s"
    else:
        return f"{value_seconds * 1000:.2f}", "ms"  # Default to ms


def measure_performance(
    log_level: int = logging.DEBUG,
    include_memory: bool = True,
    include_args: bool = False,
    threshold_ms: float = 0.0
):
    """
    Decorator to measure function execution time and memory usage
    
    Args:
        log_level: Logging level for performance logs
        include_memory: Whether to measure memory usage
        include_args: Whether to include function arguments in logs
        threshold_ms: Only log if execution time exceeds this threshold (in milliseconds)
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            func_name = _format_func_name(func)
            
            # Memory tracking setup
            memory_before = 0.0
            memory_peak = 0.0
            if include_memory:
                tracemalloc.start()
                memory_before = performance_metrics.process.memory_info().rss / 1024 / 1024  # MB
            
            # Timing
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                # Calculate metrics
                end_time = time.perf_counter()
                duration = end_time - start_time
                duration_ms = duration * 1000
                
                memory_delta = 0.0
                if include_memory:
                    memory_after = performance_metrics.process.memory_info().rss / 1024 / 1024  # MB
                    memory_delta = memory_after - memory_before
                    # Use the higher of before/after as the "peak" for this call
                    memory_peak = max(memory_before, memory_after)
                    tracemalloc.stop()
                
                # Record metrics
                performance_metrics.record_metric(func_name, duration, memory_delta, memory_peak)
                
                # Log if above threshold
                if duration_ms >= threshold_ms:
                    args_str = ""
                    if include_args and args:
                        args_str = f" args={args[:2]}..." if len(args) > 2 else f" args={args}"
                    
                    memory_str = ""
                    if include_memory:
                        memory_str = f" mem_delta={memory_delta:.2f}MB peak={memory_peak:.2f}MB"
                    
                    logger.log(
                        log_level,
                        f"PERF: {func_name} took {duration_ms:.2f}ms{memory_str}{args_str}"
                    )
        
        return sync_wrapper
    return decorator


def measure_async_performance(
    log_level: int = logging.DEBUG,
    include_memory: bool = True,
    include_args: bool = False,
    threshold_ms: float = 0.0
):
    """
    Decorator to measure async function execution time and memory usage
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            func_name = _format_func_name(func)
            
            # Memory tracking setup
            memory_before = 0.0
            memory_peak = 0.0
            if include_memory:
                tracemalloc.start()
                memory_before = performance_metrics.process.memory_info().rss / 1024 / 1024  # MB
            
            # Timing
            start_time = time.perf_counter()
            
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                # Calculate metrics
                end_time = time.perf_counter()
                duration = end_time - start_time
                duration_ms = duration * 1000
                
                memory_delta = 0.0
                if include_memory:
                    memory_after = performance_metrics.process.memory_info().rss / 1024 / 1024  # MB
                    memory_delta = memory_after - memory_before
                    # Use the higher of before/after as the "peak" for this call
                    memory_peak = max(memory_before, memory_after)
                    tracemalloc.stop()
                
                # Record metrics
                performance_metrics.record_metric(func_name, duration, memory_delta, memory_peak)
                
                # Log if above threshold
                if duration_ms >= threshold_ms:
                    args_str = ""
                    if include_args and args:
                        args_str = f" args={args[:2]}..." if len(args) > 2 else f" args={args}"
                    
                    memory_str = ""
                    if include_memory:
                        memory_str = f" mem_delta={memory_delta:.2f}MB peak={memory_peak:.2f}MB"
                    
                    logger.log(
                        log_level,
                        f"PERF: {func_name} took {duration_ms:.2f}ms{memory_str}{args_str}"
                    )
        
        return async_wrapper
    return decorator


def measure_batch_performance(batch_size_arg: str = "batch_size"):
    """
    Decorator specifically for batch processing functions
    Calculates per-item performance metrics
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            func_name = _format_func_name(func)
            
            # Extract batch size
            batch_size = 1
            if batch_size_arg in kwargs:
                batch_size = kwargs[batch_size_arg]
            elif args and hasattr(args[0], '__len__'):
                batch_size = len(args[0])
            
            start_time = time.perf_counter()
            tracemalloc.start()
            memory_before = performance_metrics.process.memory_info().rss / 1024 / 1024
            
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(*args, **kwargs)
                else:
                    result = func(*args, **kwargs)
                return result
            finally:
                end_time = time.perf_counter()
                duration = end_time - start_time
                
                memory_after = performance_metrics.process.memory_info().rss / 1024 / 1024
                memory_delta = memory_after - memory_before
                # Use the higher of before/after as the "peak" for this call
                memory_peak = max(memory_before, memory_after)
                tracemalloc.stop()
                
                # Calculate per-item metrics
                per_item_time = (duration * 1000) / batch_size if batch_size > 0 else 0
                per_item_memory = memory_delta / batch_size if batch_size > 0 else 0
                
                logger.info(
                    f"BATCH_PERF: {func_name} processed {batch_size} items in {duration*1000:.2f}ms "
                    f"({per_item_time:.2f}ms/item) mem_delta={memory_delta:.2f}MB "
                    f"({per_item_memory:.3f}MB/item) peak={memory_peak:.2f}MB"
                )
                
                performance_metrics.record_metric(func_name, duration, memory_delta, memory_peak)
        
        return wrapper
    return decorator


def get_performance_summary(memory_unit: str = "mb", time_unit: str = "auto"):
    """Get the current performance metrics summary as Rich objects"""
    return performance_metrics.get_performance_summary(memory_unit, time_unit)


def reset_performance_metrics():
    """Reset all performance metrics"""
    performance_metrics.clear_metrics()