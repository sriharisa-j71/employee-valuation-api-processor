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
    async def process_row(self, row: tuple, api_client: APIClient) -> bool:
        """Process a single employee: Call 3 APIs, calculate valuation, validate grade"""
        row_id = row[0]
        emp_id = row[1]
        emp_name = row[2]
        emp_type = row[3]
        dept = row[4]
        expected_grade = row[5]
        
        api_config = self.config.api
        base_url = api_config.get("base_url", "http://localhost:8080")
        
        try:
            # Step 1: Call API1 - Salary Data
            url1 = base_url + api_config["endpoint_salary"].format(emp_id=emp_id)
            logger.info(f"Row {row_id} ({emp_id}): Calling Salary API...")
            salary_data = await api_client.call_with_retry(url1, row_id, "salary")
            
            # Step 2: Call API2 - Loans Data
            url2 = base_url + api_config["endpoint_loans"].format(emp_id=emp_id)
            logger.info(f"Row {row_id} ({emp_id}): Calling Loans API...")
            loans_data = await api_client.call_with_retry(url2, row_id, "loans")
            
            # Step 3: Call API3 - Awards Data
            url3 = base_url + api_config["endpoint_awards"].format(emp_id=emp_id)
            logger.info(f"Row {row_id} ({emp_id}): Calling Awards API...")
            awards_data = await api_client.call_with_retry(url3, row_id, "awards")
            
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
            
            # Step 6: Update database with results
            self.database.update_success_with_results(
                row_id, valuation_index, calculated_grade, expected_grade, validation_status
            )
            
            return True
            
        except Exception as e:
            # Failure
            self.database.update_failure(row_id, str(e))
            logger.error(f"Row {row_id} ({emp_id}): ✗ Failed - {e}")
            return False
    
    @measure_batch_performance()
    async def process_batch(self, rows: list[tuple]) -> None:
        """Process a batch of rows with concurrency control"""
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
            
            # Process any exceptions that occurred
            failed_count = 0
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    row_id = rows[i][0]
                    emp_id = rows[i][1]
                    logger.error(f"Row {row_id} ({emp_id}): Unhandled exception - {result}")
                    failed_count += 1
                elif result is False:
                    failed_count += 1
            
            logger.info(f"Batch processing complete: {len(rows) - failed_count}/{len(rows)} successful")
