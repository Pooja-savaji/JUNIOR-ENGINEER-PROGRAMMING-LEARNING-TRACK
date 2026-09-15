"""
02_inheritance_and_polymorphism.py
===================================
Module 2: Object-Oriented Programming & Modular Design
Topic: Inheritance, Method Overriding, Polymorphic Dispatch, and Composition

Concepts Covered:
  - Base class `Employee` establishing shared fields and behavior
  - Subclasses: `SoftwareEngineer`, `EngineeringManager`, and `Contractor`
  - `super().__init__()` for clean, DRY initialization
  - Method overriding: `calculate_monthly_pay()`, `calculate_annual_bonus()`, `generate_payslip()`
  - Composition over Inheritance: Managers holding a collection of Employee instances
  - Polymorphic batch processing: single payroll processor dispatching to specialized subtypes
"""

from __future__ import annotations
from datetime import date
from typing import List, Optional


class Employee:
    """Base domain class representing an enterprise employee."""

    def __init__(
        self,
        emp_id: str,
        name: str,
        base_salary: float,
        department: str,
        hire_date: Optional[date] = None,
    ) -> None:
        if not emp_id or not isinstance(emp_id, str):
            raise ValueError("Employee ID must be a non-empty string.")
        if not name or not isinstance(name, str):
            raise ValueError("Employee name must be a non-empty string.")
        if base_salary < 0:
            raise ValueError("Base salary cannot be negative.")

        self._emp_id: str = emp_id.strip().upper()
        self._name: str = name.strip()
        self._base_salary: float = round(float(base_salary), 2)
        self._department: str = department.strip()
        self._hire_date: date = hire_date or date.today()

    @property
    def emp_id(self) -> str:
        return self._emp_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def base_salary(self) -> float:
        return self._base_salary

    @property
    def department(self) -> str:
        return self._department

    @property
    def hire_date(self) -> date:
        return self._hire_date

    def calculate_monthly_pay(self) -> float:
        """Standard salaried employee pay = annual base salary / 12."""
        return round(self._base_salary / 12.0, 2)

    def calculate_annual_bonus(self) -> float:
        """Standard baseline employee bonus: 5% of base salary."""
        return round(self._base_salary * 0.05, 2)

    def calculate_total_compensation(self) -> float:
        """Annual total compensation = annual base + annual bonus."""
        return round(self._base_salary + self.calculate_annual_bonus(), 2)

    def generate_payslip(self) -> str:
        """Return a formatted string representing the monthly payslip."""
        monthly = self.calculate_monthly_pay()
        bonus = round(self.calculate_annual_bonus() / 12.0, 2)
        total = round(monthly + bonus, 2)
        return (
            f"[{self.__class__.__name__}] {self._emp_id} - {self._name:<18} | "
            f"Dept: {self._department:<12} | Base: ${monthly:>8.2f} | Bonus Est: ${bonus:>7.2f} | Net: ${total:>8.2f}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self._emp_id!r}, name={self._name!r}, "
            f"dept={self._department!r}, salary=${self._base_salary:,.2f})"
        )


class SoftwareEngineer(Employee):
    """Derived engineering role with technical skillsets, leveling, and on-call stipends."""

    LEVEL_MULTIPLIERS = {
        "JUNIOR": 0.08,
        "MID": 0.12,
        "SENIOR": 0.18,
        "LEAD": 0.25,
    }

    def __init__(
        self,
        emp_id: str,
        name: str,
        base_salary: float,
        level: str = "MID",
        tech_stack: Optional[List[str]] = None,
        on_call_stipend: float = 0.0,
    ) -> None:
        super().__init__(emp_id, name, base_salary, department="Engineering")
        lvl = level.strip().upper()
        if lvl not in self.LEVEL_MULTIPLIERS:
            raise ValueError(f"Invalid engineer level: {level!r}. Allowed: {list(self.LEVEL_MULTIPLIERS.keys())}")

        self._level: str = lvl
        self._tech_stack: List[str] = list(tech_stack) if tech_stack else []
        self._on_call_stipend: float = round(float(on_call_stipend), 2)

    @property
    def level(self) -> str:
        return self._level

    @property
    def tech_stack(self) -> List[str]:
        return list(self._tech_stack)

    @property
    def on_call_stipend(self) -> float:
        return self._on_call_stipend

    def add_skill(self, skill: str) -> None:
        if skill and skill not in self._tech_stack:
            self._tech_stack.append(skill.strip())

    def calculate_monthly_pay(self) -> float:
        """Includes monthly base pay + monthly on-call compensation."""
        base_monthly = super().calculate_monthly_pay()
        return round(base_monthly + self._on_call_stipend, 2)

    def calculate_annual_bonus(self) -> float:
        """Performance bonus scaled by seniority level multiplier."""
        multiplier = self.LEVEL_MULTIPLIERS[self._level]
        return round(self._base_salary * multiplier, 2)


class EngineeringManager(Employee):
    """Manager entity demonstrating Composition over Inheritance (managing team members)."""

    def __init__(
        self,
        emp_id: str,
        name: str,
        base_salary: float,
        department: str = "Engineering",
        management_bonus_rate: float = 0.20,
    ) -> None:
        super().__init__(emp_id, name, base_salary, department=department)
        self._management_bonus_rate: float = management_bonus_rate
        # Composition: Manager HAS-A list of Employees
        self._direct_reports: List[Employee] = []

    @property
    def direct_reports(self) -> List[Employee]:
        return list(self._direct_reports)

    @property
    def team_size(self) -> int:
        return len(self._direct_reports)

    def add_report(self, employee: Employee) -> None:
        if not isinstance(employee, Employee):
            raise TypeError("Direct report must be an instance of Employee.")
        if employee.emp_id == self.emp_id:
            raise ValueError("Manager cannot report to themselves.")
        if employee not in self._direct_reports:
            self._direct_reports.append(employee)

    def remove_report(self, emp_id: str) -> bool:
        for i, emp in enumerate(self._direct_reports):
            if emp.emp_id == emp_id.strip().upper():
                del self._direct_reports[i]
                return True
        return False

    def calculate_team_payroll_budget(self) -> float:
        """Aggregated monthly payroll for manager plus all direct reports."""
        own_pay = self.calculate_monthly_pay()
        team_pay = sum(member.calculate_monthly_pay() for member in self._direct_reports)
        return round(own_pay + team_pay, 2)

    def calculate_annual_bonus(self) -> float:
        """Manager bonus = Base Bonus + Team Size Incentive ($1,500 per report)."""
        base_bonus = self._base_salary * self._management_bonus_rate
        team_incentive = len(self._direct_reports) * 1500.0
        return round(base_bonus + team_incentive, 2)


class Contractor(Employee):
    """Hourly worker demonstrating alternative pay structure without salaried base."""

    def __init__(
        self,
        emp_id: str,
        name: str,
        hourly_rate: float,
        hours_worked_this_month: float = 0.0,
        agency_fee: float = 0.0,
    ) -> None:
        # Base salary is $0 because contractor compensation is purely hourly
        super().__init__(emp_id, name, base_salary=0.0, department="Contracting")
        if hourly_rate <= 0:
            raise ValueError("Hourly rate must be positive.")
        self._hourly_rate: float = round(float(hourly_rate), 2)
        self._hours_worked: float = round(float(hours_worked_this_month), 2)
        self._agency_fee: float = round(float(agency_fee), 2)

    @property
    def hourly_rate(self) -> float:
        return self._hourly_rate

    @property
    def hours_worked(self) -> float:
        return self._hours_worked

    def log_hours(self, hours: float) -> None:
        if hours < 0:
            raise ValueError("Logged hours cannot be negative.")
        self._hours_worked += round(float(hours), 2)

    def reset_monthly_hours(self) -> None:
        self._hours_worked = 0.0

    def calculate_monthly_pay(self) -> float:
        """Contractor monthly pay = Hourly Rate * Hours Worked + Agency Fee."""
        return round((self._hourly_rate * self._hours_worked) + self._agency_fee, 2)

    def calculate_annual_bonus(self) -> float:
        """Contractors do not receive standard annual corporate bonuses."""
        return 0.0

    def generate_payslip(self) -> str:
        """Custom payslip reflecting billed hours."""
        total = self.calculate_monthly_pay()
        return (
            f"[Contractor       ] {self._emp_id} - {self._name:<18} | "
            f"Billed: {self._hours_worked:>5.1f}h @ ${self._hourly_rate:>5.2f}/h | "
            f"Bonus Est: $   0.00 | Net: ${total:>8.2f}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# POLYMORPHIC PAYROLL PROCESSOR
# ─────────────────────────────────────────────────────────────────────────────

def process_company_payroll(staff: List[Employee]) -> None:
    """Polymorphic processor: operates on Employee abstraction without type inspection."""
    w = 90
    print("=" * w)
    print("  ENTERPRISE POLYMORPHIC PAYROLL REPORT")
    print("=" * w)

    total_monthly_payout = 0.0
    total_annual_bonus_reserve = 0.0

    for emp in staff:
        # Polymorphic dispatch: correct subclass method is dynamically resolved
        monthly_pay = emp.calculate_monthly_pay()
        annual_bonus = emp.calculate_annual_bonus()

        total_monthly_payout += monthly_pay
        total_annual_bonus_reserve += annual_bonus

        print(f"  {emp.generate_payslip()}")

    print("-" * w)
    print(f"  Total Active Staff               : {len(staff)}")
    print(f"  Monthly Payroll Expenditure      : ${total_monthly_payout:>12,.2f}")
    print(f"  Estimated Annual Bonus Liability : ${total_annual_bonus_reserve:>12,.2f}")
    print("=" * w)


def main():
    print("=" * 70)
    print("  EXERCISE 02: INHERITANCE, POLYMORPHISM & COMPOSITION")
    print("=" * 70)

    # 1. Instantiate specialized roles
    eng1 = SoftwareEngineer(
        "ENG-001", "Devin Chen", base_salary=115000, level="SENIOR",
        tech_stack=["Python", "FastAPI", "Docker"], on_call_stipend=600.0
    )
    eng2 = SoftwareEngineer(
        "ENG-002", "Maya Patel", base_salary=85000, level="MID",
        tech_stack=["Python", "React", "PostgreSQL"], on_call_stipend=300.0
    )
    eng3 = SoftwareEngineer(
        "ENG-003", "Lucas Silva", base_salary=65000, level="JUNIOR",
        tech_stack=["Python", "Git"]
    )

    manager = EngineeringManager("MGR-101", "Sarah Connor", base_salary=145000)

    # Composition: Attach engineers as direct reports to the manager
    manager.add_report(eng1)
    manager.add_report(eng2)
    manager.add_report(eng3)

    contractor1 = Contractor("CTR-501", "Alex Vance", hourly_rate=85.0, hours_worked_this_month=160.0)
    contractor2 = Contractor("CTR-502", "Vikram Rao", hourly_rate=110.0, hours_worked_this_month=120.0)

    # 2. Inspect Manager & Composition
    print(f"\n[1] Composition in Action (Engineering Manager Team):")
    print(f"  Manager: {manager.name} ({manager.emp_id})")
    print(f"  Team Size: {manager.team_size} direct reports")
    for r in manager.direct_reports:
        print(f"    -> {r.name} ({r.__class__.__name__})")
    print(f"  Total Monthly Team Budget (Manager + Staff): ${manager.calculate_team_payroll_budget():,.2f}")

    # 3. Polymorphic Batch Payroll Run
    print(f"\n[2] Polymorphic Payroll Batch Execution:")
    company_staff: List[Employee] = [manager, eng1, eng2, eng3, contractor1, contractor2]
    process_company_payroll(company_staff)

    # 4. Total compensation comparison
    print(f"\n[3] Total Annual Compensation Breakdown:")
    for emp in [manager, eng1, eng2, contractor1]:
        print(f"  {emp.name:<15} ({emp.__class__.__name__:<18}): ${emp.calculate_total_compensation():>10,.2f}")

    print("\nInheritance and polymorphism demonstration complete!\n")


if __name__ == "__main__":
    main()
