
checklist = [
    "Code tested",
    "All tests passed",
    "Installation verified",
    "Uninstallation verified",
    "README updated"
]
print("Release Validation Checklist")
for item in checklist:
    print("[ ]", item)
answer = input("Is everything ready for release? (yes/no): ")

if answer.lower() == "yes":
    print("Release validated successfully!")
else:
    print("Release is not ready!")
