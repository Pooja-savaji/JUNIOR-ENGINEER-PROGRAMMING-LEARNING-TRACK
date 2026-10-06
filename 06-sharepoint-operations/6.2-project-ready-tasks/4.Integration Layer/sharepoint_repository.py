
class SharePointRepository:

    def __init__(self):
        self.items = []

    # CREATE
    def create_item(self, item):
        self.items.append(item)
        return "Item created successfully"

    # READ
    def get_items(self):
        return self.items

    def get_item(self, employee_id):
        for item in self.items:
            if item["Employee ID"] == employee_id:
                return item
        return "Item not found"

    # UPDATE
    def update_item(self, employee_id, new_status):
        for item in self.items:
            if item["Employee ID"] == employee_id:
                item["Training Status"] = new_status
                return "Item updated successfully"
        return "Item not found"

    # DELETE
    def delete_item(self, employee_id):
        for item in self.items:
            if item["Employee ID"] == employee_id:
                self.items.remove(item)
                return "Item deleted successfully"
        return "Item not found"


# Business/UI code uses the repository
repository = SharePointRepository()

employee = {
    "Employee ID": 101,
    "Employee Name": "Pooja",
    "Department": "IT",
    "Training Status": "In Progress"
}

print(repository.create_item(employee))
print(repository.get_items())

print(repository.update_item(101, "Completed"))
print(repository.get_item(101))

print(repository.delete_item(101))
print(repository.get_items())
