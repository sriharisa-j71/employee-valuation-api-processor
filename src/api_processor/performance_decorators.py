"""Performance measurement decorators for timing and memory profiling"""
import asyncio
import functools
import json
import logging
import os
import time
import tracemalloc
from pathlib import Path
from typing import Any, Callable, Dict, Optional
import psutil
from rich.console import Console
from rich.table import Table
from .emoji_support import emoji_handler

logger = logging.getLogger(__name__)

# Persistent metrics file
METRICS_FILE = Path("performance_metrics.json")
console = Console()


class PerformanceMetrics:
    """Centralized performance metrics collection with persistence"""
    
    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}
        self.process = psutil.Process(os.getpid())
        self.load_metrics()
    
    def load_metrics(self):
        """Load metrics from persistent storage"""
        try:
            if METRICS_FILE.exists():
                with open(METRICS_FILE, 'r') as f:
                    self.metrics = json.load(f)
        except Exception as e:
            logger.debug(f"Could not load metrics file: {e}")
            self.metrics = {}
    
    def save_metrics(self):
        """Save metrics to persistent storage"""
        try:
            with open(METRICS_FILE, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.debug(f"Could not save metrics file: {e}")
    
    def record_metric(self, func_name: str, duration: float, memory_delta: float, memory_peak: float):
        """Record performance metrics for a function"""
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
        metrics['peak_memory'] = max(metrics['peak_memory'], memory_peak)
        
        # Save after each update for persistence
        self.save_metrics()
    
    def get_performance_summary(self) -> str:
        """Generate comprehensive performance summary using Rich formatting"""
        if not self.metrics:
            return emoji_handler.format_message("info", "[yellow]No performance metrics available[/yellow]")
        
        # Create Rich table
        table = Table(show_header=True, header_style="bold magenta", title=emoji_handler.format_message("performance", "Performance Metrics Report"))
        table.add_column("Function", style="cyan", no_wrap=False, min_width=30)
        table.add_column("Calls", justify="right", style="green")
        table.add_column("Avg Time (ms)", justify="right", style="yellow")
        table.add_column("Min Time (ms)", justify="right", style="blue")
        table.add_column("Max Time (ms)", justify="right", style="blue")
        table.add_column("Total Time (s)", justify="right", style="red")
        table.add_column("Avg Mem (MB)", justify="right", style="cyan")
        table.add_column("Peak Mem (MB)", justify="right", style="magenta")
        
        # Sort by total time descending
        sorted_metrics = sorted(self.metrics.items(), key=lambda x: x[1]['total_time'], reverse=True)
        
        for func_name, metrics in sorted_metrics:
            avg_time_ms = (metrics['total_time'] / metrics['calls']) * 1000
            min_time_ms = metrics['min_time'] * 1000
            max_time_ms = metrics['max_time'] * 1000
            total_time_s = metrics['total_time']
            
            # Truncate long function names for better display
            display_name = func_name
            if len(display_name) > 50:
                display_name = "..." + display_name[-47:]
            
            table.add_row(
                display_name,
                str(metrics['calls']),
                f"{avg_time_ms:.2f}",
                f"{min_time_ms:.2f}",
                f"{max_time_ms:.2f}",
                f"{total_time_s:.3f}",
                f"{metrics['avg_memory']:.2f}",
                f"{metrics['peak_memory']:.2f}"
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
            short_name = func_name.split('.')[-2:] if '.' in func_name else [func_name]
            short_name = '.'.join(short_name)
            time_style = "red" if metrics['total_time'] > 0.1 else "yellow" if metrics['total_time'] > 0.01 else "green"
            slowest_table.add_row(
                f"{i}.",
                short_name,
                f"[{time_style}]{metrics['total_time']*1000:.1f}ms[/{time_style}] total ({metrics['calls']} calls)"
            )
        
        # Render everything to string
        from io import StringIO
        string_console = Console(file=StringIO(), width=120)
        
        string_console.print(table)
        string_console.print(f"\n[bold cyan]{emoji_handler.format_message('info', 'Performance Summary Statistics')}[/bold cyan]")
        string_console.print(summary_table)
        string_console.print(f"\n[bold red]{emoji_handler.format_message('info', 'Top 3 Slowest Functions (by total time)')}[/bold red]")
        string_console.print(slowest_table)
        
        return string_console.file.getvalue()
    
    def clear_metrics(self):
        """Clear all metrics"""
        self.metrics.clear()
        try:
            if METRICS_FILE.exists():
                METRICS_FILE.unlink()
        except Exception as e:
            logger.debug(f"Could not delete metrics file: {e}")


# Global metrics instance
performance_metrics = PerformanceMetrics()


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
            func_name = f"{func.__module__}.{func.__qualname__}"
            
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
                    
                    current, peak = tracemalloc.get_traced_memory()
                    memory_peak = peak / 1024 / 1024  # Convert to MB
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
            func_name = f"{func.__module__}.{func.__qualname__}"
            
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
                    
                    current, peak = tracemalloc.get_traced_memory()
                    memory_peak = peak / 1024 / 1024  # Convert to MB
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
            func_name = f"{func.__module__}.{func.__qualname__}"
            
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
                current, peak = tracemalloc.get_traced_memory()
                memory_peak = peak / 1024 / 1024
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


def get_performance_summary() -> str:
    """Get the current performance metrics summary"""
    return performance_metrics.get_performance_summary()


def reset_performance_metrics():
    """Reset all performance metrics"""
    performance_metrics.clear_metrics()