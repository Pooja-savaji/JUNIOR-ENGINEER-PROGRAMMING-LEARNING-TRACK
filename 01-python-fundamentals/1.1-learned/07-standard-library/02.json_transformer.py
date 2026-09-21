import json

with open("sample.json", "r") as file:
    students = json.load(file)

for student in students:
    student["status"] = "Active"

with open("updated_students.json", "w") as file:
    json.dump(students, file, indent=4)

print("JSON file updated successfully.")
