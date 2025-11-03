"""Processing orchestration"""
import asyncio
import logging
from typing import Any

from .api_client import APIClient
from .config import Config
from .database import Database
from .valuation import EmployeeValuator
from .performance_decorators import measure_async_performance, measure_batch_performance

logger = logging.getLogger(__name__)


class Orchestrator:
    """Orchestrates the processing of rows"""
    
    def __init__(self, config: Config, database: Database):
        self.config = config
        self.database = database
        self.valuator = EmployeeValuator(config._config.get("valuation", {}))
    
    @measure_async_performance(include_memory=True, threshold_ms=100.0, include_args=True)
    async def process_row(self, row: tuple, api_client: APIClient) -> dict:
        """Process a single employee: Call 3 APIs, calculate valuation, validate grade
        Returns result dict instead of updating database directly for batch processing"""
        row_id = row[0]
        emp_id = row[1]
        emp_name = row[2]
        emp_type = row[3]
        dept = row[4]
        expected_grade = row[5]
        
        api_config = self.config.api
        
        # Multi-host URL construction - each API can be on different hosts
        salary_base = api_config.get("salary_base_url", api_config.get("base_url", "http://localhost:8080"))
        loans_base = api_config.get("loans_base_url", api_config.get("base_url", "http://localhost:8080"))
        awards_base = api_config.get("awards_base_url", api_config.get("base_url", "http://localhost:8080"))
        
        try:
            # API Chain: API1 -> API2 -> API3 (each depends on the previous)
            # Each API potentially on different hosts for production scalability
            
            # Step 1: Call API1 - Salary Data (independent)
            url1 = salary_base + api_config["endpoint_salary"].format(emp_id=emp_id)
            logger.debug(f"Row {row_id} ({emp_id}): Calling Salary API at {salary_base}...")
            salary_data = await api_client.call_with_retry(url1, row_id, "salary")
            
            # Step 2: Call API2 - Loans Data (requires salary token)
            url2 = loans_base + api_config["endpoint_loans"].format(emp_id=emp_id)
            logger.debug(f"Row {row_id} ({emp_id}): Calling Loans API at {loans_base}...")
            
            # Extract salary token for API2 dependency
            loans_headers = {}
            if '_salary_token' in salary_data:
                loans_headers['X-Salary-Token'] = salary_data['_salary_token']
            
            loans_data = await api_client.call_with_retry(url2, row_id, "loans", loans_headers)
            
            # Step 3: Call API3 - Awards Data (requires loan token)
            url3 = awards_base + api_config["endpoint_awards"].format(emp_id=emp_id)
            logger.debug(f"Row {row_id} ({emp_id}): Calling Awards API at {awards_base}...")
            
            # Extract loan token for API3 dependency
            awards_headers = {}
            if '_loan_token' in loans_data:
                awards_headers['X-Loan-Token'] = loans_data['_loan_token']
            
            awards_data = await api_client.call_with_retry(url3, row_id, "awards", awards_headers)
            
            # Step 4: Calculate valuation index
            valuation_index = self.valuator.calculate_index(salary_data, loans_data, awards_data)
            calculated_grade = self.valuator.calculate_grade(valuation_index)
            
            # Step 5: Validate against expected grade
            validation_status = "PASS" if calculated_grade == expected_grade else "FAIL"
            
            logger.info(
                f"Row {row_id} ({emp_id}): Index={valuation_index}, "
                f"Calculated={calculated_grade}, Expected={expected_grade}, "
                f"Status={validation_status}"
            )
            
            # Return success result for batch update
            return {
                'success': True,
                'row_id': row_id,
                'valuation_index': valuation_index,
                'calculated_grade': calculated_grade,
                'expected_grade': expected_grade,
                'validation_status': validation_status
            }
            
        except Exception as e:
            # Return failure result for batch update
            logger.error(f"Row {row_id} ({emp_id}): ✗ Failed - {e}")
            return {
                'success': False,
                'row_id': row_id,
                'error': str(e)
            }
    
    @measure_batch_performance()
    async def process_batch(self, rows: list[tuple]) -> None:
        """Process a batch of rows with concurrency control and batch database updates"""
        if not rows:
            logger.info("No rows to process")
            return
        
        concurrency = self.config.concurrency
        semaphore = asyncio.Semaphore(concurrency)
        
        logger.info(f"Processing {len(rows)} rows with concurrency={concurrency}...")
        
        async with APIClient(self.config) as api_client:
            async def process_with_semaphore(row):
                async with semaphore:
                    return await self.process_row(row, api_client)
            
            tasks = [process_with_semaphore(row) for row in rows]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Collect all results for batch database update
            batch_results = []
            failed_count = 0
            exception_count = 0
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    row_id = rows[i][0]
                    emp_id = rows[i][1]
                    logger.error(f"Row {row_id} ({emp_id}): Unhandled exception - {result}")
                    batch_results.append({
                        'success': False,
                        'row_id': row_id,
                        'error': str(result)
                    })
                    exception_count += 1
                else:
                    batch_results.append(result)
                    if not result.get('success', False):
                        failed_count += 1
            
            # Batch update database with all results
            if batch_results:
                self.database.batch_update_results(batch_results)
            
            total_failed = failed_count + exception_count
            logger.info(f"Batch processing complete: {len(rows) - total_failed}/{len(rows)} successful")
