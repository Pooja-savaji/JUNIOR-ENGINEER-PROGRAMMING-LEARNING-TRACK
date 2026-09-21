"""Simple Employee Directory and Analytics System (Beginner Friendly).

Demonstrates:
- Dictionary-based record management
- Department grouping, salary statistics, and search operations
- Add, update, and search functionality
"""


class EmployeeDirectory:
    """Manages company staff members and departmental statistics."""

    def __init__(self):
        # Sample starter employees
        self.employees = [
            {"id": 101, "name": "Pooja Savaji", "dept": "Engineering", "role": "Software Engineer", "salary": 85000},
            {"id": 102, "name": "John Doe", "dept": "Engineering", "role": "Senior Developer", "salary": 110000},
            {"id": 103, "name": "Sarah Connor", "dept": "Marketing", "role": "Marketing Lead", "salary": 75000},
            {"id": 104, "name": "Michael Scott", "dept": "Sales", "role": "Regional Manager", "salary": 90000},
            {"id": 105, "name": "Jim Halpert", "dept": "Sales", "role": "Sales Representative", "salary": 65000},
            {"id": 106, "name": "Pam Beesly", "dept": "HR", "role": "HR Specialist", "salary": 60000},
        ]

    def add_employee(self, name: str, dept: str, role: str, salary: float) -> dict:
        """Add a new employee with an auto-generated unique ID."""
        new_id = max(e["id"] for e in self.employees) + 1 if self.employees else 101
        new_emp = {
            "id": new_id,
            "name": name.strip(),
            "dept": dept.strip(),
            "role": role.strip(),
            "salary": float(salary),
        }
        self.employees.append(new_emp)
        print(f"[Success] Added employee: {new_emp['name']} (ID: {new_emp['id']})")
        return new_emp

    def list_employees(self, emp_list=None):
        """Display employees in a formatted table."""
        display = emp_list if emp_list is not None else self.employees
        print("\n" + "=" * 70)
        print(f"{'ID':<5} | {'Name':<18} | {'Department':<14} | {'Role':<20} | {'Salary':>9}")
        print("=" * 70)
        if not display:
            print("  [No employees found]")
        else:
            for e in display:
                print(f"{e['id']:<5} | {e['name']:<18} | {e['dept']:<14} | {e['role']:<20} | ${e['salary']:>8,.2f}")
        print("=" * 70)

    def search_by_name(self, keyword: str) -> list:
        """Find employees whose name contains the keyword (case-insensitive)."""
        clean_kw = keyword.strip().lower()
        return [e for e in self.employees if clean_kw in e["name"].lower()]

    def filter_by_department(self, department: str) -> list:
        """Get all employees in a specific department."""
        clean_dept = department.strip().lower()
        return [e for e in self.employees if e["dept"].lower() == clean_dept]

    def get_department_analytics(self) -> dict:
        """Calculate headcount, total salary, and average salary per department."""
        dept_data = {}

        for e in self.employees:
            dept = e["dept"]
            sal = e["salary"]
            if dept not in dept_data:
                dept_data[dept] = {"headcount": 0, "total_salary": 0.0}
            dept_data[dept]["headcount"] += 1
            dept_data[dept]["total_salary"] += sal

        # Calculate averages
        for dept, stats in dept_data.items():
            stats["avg_salary"] = round(stats["total_salary"] / stats["headcount"], 2)

        return dept_data

    def get_highest_paid_employee(self) -> dict:
        """Find the employee with the highest salary."""
        if not self.employees:
            return {}
        return max(self.employees, key=lambda e: e["salary"])


def run_employee_demo():
    print("=" * 55)
    print("         👥 EMPLOYEE DIRECTORY DEMO            ")
    print("=" * 55)

    directory = EmployeeDirectory()

    # 1. View all employees
    print("\n1. Complete Employee Directory:")
    directory.list_employees()

    # 2. Department Analytics
    print("\n2. Department-wise Analytics:")
    analytics = directory.get_department_analytics()
    print("-" * 55)
    print(f"{'Department':<16} | {'Headcount':<10} | {'Average Salary':>15}")
    print("-" * 55)
    for dept, data in analytics.items():
        print(f"{dept:<16} | {data['headcount']:<10} | ${data['avg_salary']:>14,.2f}")
    print("-" * 55)

    # 3. Highest Paid
    top_earner = directory.get_highest_paid_employee()
    print(f"\nHighest Paid Employee: {top_earner['name']} (${top_earner['salary']:,.2f} - {top_earner['role']})")

    # 4. Search
    print("\n3. Search for 'John':")
    results = directory.search_by_name("John")
    directory.list_employees(results)


if __name__ == "__main__":
    run_employee_demo()
