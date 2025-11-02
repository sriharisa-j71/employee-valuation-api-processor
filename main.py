#!/usr/bin/env python3
"""Entry point for the API processor application"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from api_processor.main import app

if __name__ == "__main__":
    app()