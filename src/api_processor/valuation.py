"""Employee valuation calculation logic"""
from typing import Any

from .performance_decorators import measure_performance


class ValidationError(Exception):
    """Valuation data validation errors"""
    pass


class EmployeeValuator:
    """Calculate employee valuation index and grade"""
    
    def __init__(self, config: dict[str, Any]):
        self.grade_a_min = config.get("grade_a_min", 80)
        self.grade_b_min = config.get("grade_b_min", 60)
        self.grade_c_min = config.get("grade_c_min", 40)
    
    def _safe_float(self, value: Any, field_name: str, default: float = 0.0) -> float:
        """Safely convert a value to float with validation"""
        if value is None:
            return default
        
        try:
            result = float(value)
            if result < 0 and field_name not in ["outstanding_amount"]:  # outstanding can be negative
                raise ValidationError(f"{field_name} cannot be negative: {result}")
            return result
        except (TypeError, ValueError) as e:
            raise ValidationError(f"Invalid {field_name} value '{value}': {e}")

    @measure_performance(include_memory=True, threshold_ms=5.0, include_args=True)
    def calculate_index(
        self,
        salary_data: dict[str, Any],
        loans_data: dict[str, Any],
        awards_data: dict[str, Any]
    ) -> float:
        """
        Calculate valuation index based on multiple factors
        
        Formula:
        - Salary component: 30% (normalized base_salary + bonus)
        - Service component: 15% (years_of_service)
        - Loan component: 20% (repayment_score - penalty for outstanding)
        - Awards component: 35% (awards + recognitions + performance)
        """
        # Validate and extract data with type safety
        base_salary = self._safe_float(salary_data.get("base_salary"), "base_salary", 50000)
        bonus = self._safe_float(salary_data.get("bonus"), "bonus", 5000)
        years_of_service = self._safe_float(salary_data.get("years_of_service"), "years_of_service", 1)
        
        repayment_score = self._safe_float(loans_data.get("repayment_score"), "repayment_score", 80)
        outstanding = self._safe_float(loans_data.get("outstanding_amount"), "outstanding_amount", 0)
        
        total_awards = self._safe_float(awards_data.get("total_awards"), "total_awards", 0)
        recognitions = self._safe_float(awards_data.get("recognitions"), "recognitions", 0)
        performance_rating = self._safe_float(awards_data.get("performance_rating"), "performance_rating", 3)
        
        # Additional validation
        if repayment_score > 100:
            raise ValidationError(f"repayment_score cannot exceed 100: {repayment_score}")
        if performance_rating > 5:
            raise ValidationError(f"performance_rating cannot exceed 5: {performance_rating}")
        
        # Salary component (max 30 points)
        salary_score = min((base_salary + bonus) / 2000, 30)
        
        # Service component (max 15 points)
        service_score = min(years_of_service * 0.75, 15)
        
        # Loan component (max 20 points)
        loan_penalty = min(abs(outstanding) / 5000, 10)  # Max 10 point penalty
        loan_score = max((repayment_score / 5) - loan_penalty, 0)
        
        # Awards component (max 35 points)
        awards_score = min((total_awards * 2) + (recognitions * 0.5) + (performance_rating * 3), 35)
        
        # Total index (0-100)
        total_index = salary_score + service_score + loan_score + awards_score
        return round(total_index, 2)
    
    @measure_performance(include_memory=False, threshold_ms=1.0)
    def calculate_grade(self, valuation_index: float) -> str:
        """Determine grade based on valuation index"""
        if valuation_index >= self.grade_a_min:
            return "A"
        elif valuation_index >= self.grade_b_min:
            return "B"
        elif valuation_index >= self.grade_c_min:
            return "C"
        else:
            return "D"
