def find_employee(employees, emp_id):
    return employees.get(emp_id, "Employee not found")


employees = {
    "101": "Pooja",
    "102": "Rahul",
    "103": "Sneha"
}

emp_id = input("Enter employee ID: ")

print("Employee:", find_employee(employees, emp_id))
