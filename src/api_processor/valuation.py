"""Employee valuation calculation logic"""
from typing import Any


class EmployeeValuator:
    """Calculate employee valuation index and grade"""
    
    def __init__(self, config: dict[str, Any]):
        self.grade_a_min = config.get("grade_a_min", 80)
        self.grade_b_min = config.get("grade_b_min", 60)
        self.grade_c_min = config.get("grade_c_min", 40)
    
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
        # Salary component (max 30 points)
        base_salary = float(salary_data.get("base_salary", 50000))
        bonus = float(salary_data.get("bonus", 5000))
        salary_score = min((base_salary + bonus) / 2000, 30)
        
        # Service component (max 15 points)
        years_of_service = float(salary_data.get("years_of_service", 1))
        service_score = min(years_of_service * 0.75, 15)
        
        # Loan component (max 20 points)
        repayment_score = float(loans_data.get("repayment_score", 80))
        outstanding = float(loans_data.get("outstanding_amount", 0))
        loan_penalty = min(outstanding / 5000, 10)  # Max 10 point penalty
        loan_score = max((repayment_score / 5) - loan_penalty, 0)
        
        # Awards component (max 35 points)
        total_awards = float(awards_data.get("total_awards", 0))
        recognitions = float(awards_data.get("recognitions", 0))
        performance_rating = float(awards_data.get("performance_rating", 3))
        awards_score = min((total_awards * 2) + (recognitions * 0.5) + (performance_rating * 3), 35)
        
        # Total index (0-100)
        total_index = salary_score + service_score + loan_score + awards_score
        return round(total_index, 2)
    
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
