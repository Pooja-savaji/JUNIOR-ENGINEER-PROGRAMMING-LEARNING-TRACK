
class Employee:
    def __init__(self, employee_id, name, department, training, status):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.training = training
        self.status = status

    def to_sharepoint(self):
        return {
            "Employee ID": self.employee_id,
            "Employee Name": self.name,
            "Department": self.department,
            "Training Name": self.training,
            "Training Status": self.status
        }

# SharePoint list simulation
employees = []

# CREATE
employee = Employee(101, "Pooja", "IT", "Python", "In Progress")
employees.append(employee.to_sharepoint())
print("Created:", employees[0])

# READ
print("Read:", employees[0])

# UPDATE
employees[0]["Training Status"] = "Completed"
print("Updated:", employees[0])

# DELETE
deleted_employee = employees.pop(0)
print("Deleted:", deleted_employee)

# Final data
print("Final SharePoint List:", employees)
