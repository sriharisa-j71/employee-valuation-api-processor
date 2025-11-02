"""CLI entry point"""
import asyncio
import logging
import sys

import typer

from .config import Config
from .database import Database
from .orchestrator import Orchestrator

app = typer.Typer()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@app.command()
def load(file: str = typer.Argument(..., help="Path to input pipe-separated file")):
    """Load employee data from file into DuckDB"""
    config = Config()
    db = Database(config.db_path)
    
    try:
        total = db.load_data(file)
        logger.info(f"✓ Successfully loaded {total} employee records")
    finally:
        db.close()


@app.command()
def process(
    start: int = typer.Option(None, help="Start line number (inclusive)"),
    end: int = typer.Option(None, help="End line number (inclusive)"),
    reset_failed: bool = typer.Option(False, help="Reset failed records to pending")
):
    """Process employee records and validate grades"""
    config = Config()
    db = Database(config.db_path)
    
    try:
        if reset_failed:
            db.reset_failed()
            logger.info("Reset failed records to pending")
        
        # Get pending rows
        pending_rows = db.get_pending_rows(start, end)
        
        if not pending_rows:
            logger.info("No pending records to process")
            return
        
        # Log range info
        if start and end:
            logger.info(f"Processing lines {start} to {end}...")
        elif start:
            logger.info(f"Processing lines from {start} onwards...")
        elif end:
            logger.info(f"Processing lines up to {end}...")
        else:
            logger.info("Processing all pending lines...")
        
        # Process batch
        orchestrator = Orchestrator(config, db)
        asyncio.run(orchestrator.process_batch(pending_rows))
        
        # Check failure threshold
        total_failures = db.get_failure_count()
        if total_failures >= config.max_failures:
            logger.critical(f"✗ Failure limit exceeded ({total_failures}/{config.max_failures}). Exiting.")
            sys.exit(1)
        
        logger.info("✓ Processing complete")
        
    finally:
        db.close()


@app.command()
def status(
    start: int = typer.Option(None, help="Start line number for filtered status"),
    end: int = typer.Option(None, help="End line number for filtered status")
):
    """Show processing status summary"""
    config = Config()
    db = Database(config.db_path)
    
    try:
        summary = db.get_status_summary(start, end)
        total = db.get_total_count(start, end)
        
        # Build title
        if start and end:
            title = f"Processing Status (Lines {start}-{end})"
        elif start:
            title = f"Processing Status (Lines {start}+)"
        elif end:
            title = f"Processing Status (Lines up to {end})"
        else:
            title = "Processing Status (All Lines)"
        
        print(f"\n=== {title} ===")
        for status, count in summary:
            percentage = (count / total * 100) if total > 0 else 0
            print(f"{status:10s}: {count:6d} ({percentage:5.1f}%)")
        print(f"{'Total':10s}: {total:6d}")
        print()
        
    finally:
        db.close()


@app.command()
def report():
    """Generate validation report"""
    config = Config()
    db = Database(config.db_path)
    
    try:
        # Validation summary
        print("\n=== Validation Summary ===")
        validation_summary = db.get_validation_summary()
        for validation_status, count, avg_index in validation_summary:
            print(f"{validation_status:10s}: {count:4d} records (Avg Index: {avg_index})")
        
        # Grade distribution
        print("\n=== Grade Distribution ===")
        grade_dist = db.get_grade_distribution()
        for grade, count in grade_dist:
            print(f"Grade {grade}: {count:4d} employees")
        
        # Mismatches
        print("\n=== Validation Failures (Grade Mismatches) ===")
        mismatches = db.get_mismatches()
        if mismatches:
            print(f"{'Emp ID':<10} {'Name':<20} {'Index':<8} {'Calculated':<12} {'Expected':<10}")
            print("-" * 70)
            for emp_id, emp_name, index, calc_grade, exp_grade in mismatches:
                print(f"{emp_id:<10} {emp_name:<20} {index:<8.2f} {calc_grade:<12} {exp_grade:<10}")
        else:
            print("✓ No mismatches found - all validations passed!")
        print()
        
    finally:
        db.close()


@app.command()
def reset(
    start: int = typer.Option(None, help="Start line number"),
    end: int = typer.Option(None, help="End line number")
):
    """Reset records to pending status"""
    config = Config()
    db = Database(config.db_path)
    
    try:
        db.reset_range(start, end)
        
        if start and end:
            logger.info(f"✓ Reset lines {start}-{end} to pending")
        elif start:
            logger.info(f"✓ Reset lines {start}+ to pending")
        elif end:
            logger.info(f"✓ Reset lines up to {end} to pending")
        else:
            logger.info("✓ Reset all lines to pending")
    finally:
        db.close()


if __name__ == "__main__":
    app()
