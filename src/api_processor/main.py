"""CLI entry point"""
import asyncio
import logging
import sys

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from .config import Config, ConfigError
from .database import Database
from .orchestrator import Orchestrator
from .performance_decorators import get_performance_summary, reset_performance_metrics
from .emoji_support import emoji_handler
from tabulate import tabulate

app = typer.Typer()
console = Console()

# Configure file logging
file_handler = logging.FileHandler('employee_processor.log')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
file_handler.setFormatter(file_formatter)

# Configure console logging with Rich (for user-facing messages only)
console_handler = RichHandler(console=console, rich_tracebacks=True)
console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[file_handler, console_handler]
)
logger = logging.getLogger(__name__)


@app.command()
def load(file: str = typer.Argument(..., help="Path to input pipe-separated file")):
    """Load employee data from file into DuckDB"""
    try:
        config = Config()
    except ConfigError as e:
        console.print(f"{emoji_handler.get_status_icon('error')} [red]Configuration error:[/red] {e}")
        sys.exit(1)
    
    db = Database(config)
    
    try:
        console.print(emoji_handler.format_message("loading", f"[cyan]Loading data from[/cyan] {file}..."))
        total = db.load_data(file)
        console.print(emoji_handler.format_message("complete", f"[green]Successfully loaded[/green] [bold]{total:,}[/bold] [cyan]employee records[/cyan]"))
    except Exception as e:
        console.print(f"{emoji_handler.get_status_icon('error')} [red]Failed to load data:[/red] {e}")
        sys.exit(1)
    finally:
        db.close()


@app.command()
def process(
    start: int = typer.Option(None, help="Start line number (inclusive)"),
    end: int = typer.Option(None, help="End line number (inclusive)"),
    reset_failed: bool = typer.Option(False, help="Reset failed records to pending")
):
    """Process employee records and validate grades"""
    try:
        config = Config()
    except ConfigError as e:
        console.print(f"{emoji_handler.get_status_icon('error')} [red]Configuration error:[/red] {e}")
        sys.exit(1)
    
    db = Database(config)
    
    try:
        if reset_failed:
            db.reset_failed()
            console.print(emoji_handler.format_message("reset", "[yellow]Reset failed records to pending[/yellow]"))
        
        # Get pending rows
        pending_rows = db.get_pending_rows(start, end)
        
        if not pending_rows:
            console.print(f"{emoji_handler.get_status_icon('info')} [blue]No pending records to process[/blue]")
            return
        
        # Log range info
        if start and end:
            console.print(emoji_handler.format_message("processing", f"[cyan]Processing lines[/cyan] [bold]{start}[/bold] [cyan]to[/cyan] [bold]{end}[/bold]..."))
        elif start:
            console.print(emoji_handler.format_message("processing", f"[cyan]Processing lines from[/cyan] [bold]{start}[/bold] [cyan]onwards...[/cyan]"))
        elif end:
            console.print(emoji_handler.format_message("processing", f"[cyan]Processing lines up to[/cyan] [bold]{end}[/bold]..."))
        else:
            console.print(emoji_handler.format_message("processing", "[cyan]Processing all pending lines...[/cyan]"))
        
        # Process batch
        orchestrator = Orchestrator(config, db)
        asyncio.run(orchestrator.process_batch(pending_rows))
        
        # Check failure threshold
        total_failures = db.get_failure_count()
        if total_failures >= config.max_failures:
            console.print(f"{emoji_handler.get_status_icon('error')} [red]Failure limit exceeded[/red] ([bold]{total_failures}/{config.max_failures}[/bold]). [red]Exiting.[/red]")
            sys.exit(1)
        
        console.print(emoji_handler.format_message("complete", "[green]Processing complete[/green]"))
        
    finally:
        db.close()


@app.command()
def status(
    start: int = typer.Option(None, help="Start line number for filtered status"),
    end: int = typer.Option(None, help="End line number for filtered status")
):
    """Show processing status summary"""
    config = Config()
    db = Database(config)
    
    try:
        summary = db.get_status_summary(start, end)
        total = db.get_total_count(start, end)
        
        # Build title
        if start and end:
            title_text = f"Processing Status (Lines {start}-{end})"
        elif start:
            title_text = f"Processing Status (Lines {start}+)"
        elif end:
            title_text = f"Processing Status (Lines up to {end})"
        else:
            title_text = "Processing Status (All Lines)"
        
        title = emoji_handler.format_message("validation", title_text)
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
        
        # Create Rich table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Status", style="cyan", no_wrap=True)
        table.add_column("Count", justify="right", style="green")
        table.add_column("Percentage", justify="right", style="yellow")
        
        # Add status rows with emoji handler
        for status, count in summary:
            percentage = (count / total * 100) if total > 0 else 0
            status_row = emoji_handler.format_status_row(status, status.title())
            table.add_row(
                status_row, 
                f"{count:,}", 
                f"{percentage:.1f}%"
            )
        
        # Add total row
        total_row = emoji_handler.format_status_row("total", "TOTAL")
        table.add_row(total_row, f"{total:,}", "100.0%", style="bold")
        
        console.print(table)
        console.print()
        
    finally:
        db.close()


@app.command()
def report():
    """📋 Generate validation report"""
    config = Config()
    db = Database(config)
    
    try:
        # Validation summary
        title = emoji_handler.format_message("validation", "Validation Summary")
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
        validation_summary = db.get_validation_summary()
        if validation_summary:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Status", style="cyan", no_wrap=True)
            table.add_column("Count", justify="right", style="green")
            table.add_column("Avg Index", justify="right", style="yellow")
            
            for status, count, avg_index in validation_summary:
                status_row = emoji_handler.format_status_row(status, status.title())
                table.add_row(
                    status_row, 
                    f"{count:,}", 
                    f"{avg_index:.2f}" if avg_index else "N/A"
                )
            console.print(table)
        else:
            console.print(f"{emoji_handler.get_status_icon('warning')} [yellow]No validation data available[/yellow]")
        
        # Grade distribution
        title = emoji_handler.format_message("distribution", "Grade Distribution")
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
        grade_dist = db.get_grade_distribution()
        if grade_dist:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Grade", style="cyan", no_wrap=True)
            table.add_column("Count", justify="right", style="green")
            
            for grade, count in grade_dist:
                grade_row = emoji_handler.format_message("grade", f"Grade {grade}")
                table.add_row(grade_row, f"{count:,}")
            console.print(table)
        else:
            console.print(f"{emoji_handler.get_status_icon('warning')} [yellow]No grade data available[/yellow]")
        
        # Mismatches
        title = emoji_handler.format_message("failures", "Validation Failures (Grade Mismatches)")
        console.print(f"\n[bold cyan]{title}[/bold cyan]")
        mismatches = db.get_mismatches()
        if mismatches:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Employee ID", style="cyan")
            table.add_column("Name", style="white")
            table.add_column("Index", justify="right", style="yellow")
            table.add_column("Calculated", style="green")
            table.add_column("Expected", style="red")
            
            for emp_id, emp_name, index, calc_grade, exp_grade in mismatches:
                table.add_row(
                    str(emp_id),
                    emp_name[:20],
                    f"{index:.2f}",
                    calc_grade,
                    exp_grade
                )
            console.print(table)
        else:
            success_msg = emoji_handler.format_message("complete", "[bold green]No mismatches found - all validations passed![/bold green]")
            console.print(success_msg)
        console.print()
        
    finally:
        db.close()


@app.command()
def reset(
    start: int = typer.Option(None, help="Start line number"),
    end: int = typer.Option(None, help="End line number")
):
    """🔄 Reset records to pending status"""
    config = Config()
    db = Database(config)
    
    try:
        db.reset_range(start, end)
        
        if start and end:
            console.print(emoji_handler.format_message("complete", f"[bold green]Reset lines {start}-{end} to pending[/bold green]"))
        elif start:
            console.print(emoji_handler.format_message("complete", f"[bold green]Reset lines {start}+ to pending[/bold green]"))
        elif end:
            console.print(emoji_handler.format_message("complete", f"[bold green]Reset lines up to {end} to pending[/bold green]"))
        else:
            console.print(emoji_handler.format_message("complete", "[bold green]Reset all lines to pending[/bold green]"))
    finally:
        db.close()


@app.command()
def perf(
    memory_unit: str = typer.Option("mb", help="Memory unit: bytes, kb, mb, gb"),
    time_unit: str = typer.Option("auto", help="Time unit: ns, us, ms, s, auto")
):
    """📊 Show performance metrics summary"""
    # Validate units
    valid_memory_units = ["bytes", "kb", "mb", "gb"]
    valid_time_units = ["ns", "us", "ms", "s", "auto"]
    
    if memory_unit.lower() not in valid_memory_units:
        console.print(f"{emoji_handler.get_status_icon('error')} [red]Invalid memory unit. Valid options: {', '.join(valid_memory_units)}[/red]")
        raise typer.Exit(1)
    
    if time_unit.lower() not in valid_time_units:
        console.print(f"{emoji_handler.get_status_icon('error')} [red]Invalid time unit. Valid options: {', '.join(valid_time_units)}[/red]")
        raise typer.Exit(1)
    
    result = get_performance_summary(memory_unit.lower(), time_unit.lower())
    
    if result[0] is None:  # No metrics available
        console.print(result[3][0])  # Print the "no metrics" message
        return
    
    main_table, summary_table, slowest_table, title_messages = result
    
    # Print with full terminal width
    console.print(main_table)
    console.print(f"\n[bold cyan]{title_messages[0]}[/bold cyan]")
    console.print(summary_table)
    console.print(f"\n[bold red]{title_messages[1]}[/bold red]")
    console.print(slowest_table)


@app.command()
def perf_reset():
    """🔄 Reset performance metrics"""
    reset_performance_metrics()
    console.print(emoji_handler.format_message("complete", "[bold green]Performance metrics reset[/bold green]"))


if __name__ == "__main__":
    app()
