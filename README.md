# Employee Valuation API Processor

A production-ready system for processing large employee files, calling multiple REST APIs, calculating employee valuation scores, and validating grade assignments.

## 📚 CKAD Study Materials

This repository includes comprehensive study materials for the Certified Kubernetes Application Developer (CKAD) exam:
- **[CKAD-Resources.md](./CKAD-Resources.md)** - Links organized by exam domains & competencies
- **[CKAD-Common-Pitfalls.md](./CKAD-Common-Pitfalls.md)** - Common mistakes and how to avoid them
- **[CKAD-4-Day-Study-Plan.md](./CKAD-4-Day-Study-Plan.md)** - Intensive 4-day study schedule

## Features

✅ **Batch Processing** - Process large files in configurable batches by line ranges  
✅ **Concurrent API Calls** - Async HTTP with connection pooling (httpx)  
✅ **Database Control** - Track processing status with DuckDB  
✅ **Retry Logic** - Exponential backoff for failed API calls  
✅ **Mock APIs** - WireMock-based testing with Docker Compose  
✅ **Validation** - Calculate valuation index and validate employee grades  
✅ **Reporting** - Comprehensive validation reports and statistics  

## Quick Start

```bash
# Install dependencies
uv sync

# Start mock APIs
docker-compose up -d

# Load and process employee data
uv run api-processor load data/employees.txt
uv run api-processor process
uv run api-processor report
