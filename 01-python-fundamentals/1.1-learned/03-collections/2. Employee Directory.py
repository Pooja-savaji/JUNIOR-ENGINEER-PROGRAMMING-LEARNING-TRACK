employees = {
    "101": "Pooja",
    "102": "Rahul",
    "103": "Sneha"
}

emp_id = input("Enter employee ID: ")

if emp_id in employees:
    print("Employee:", employees[emp_id])
else:
    print("Employee not found")
