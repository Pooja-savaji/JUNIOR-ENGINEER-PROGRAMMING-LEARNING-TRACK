
sharepoint_structure = {
    "Site": "TechLearn Training",

    "List": {
        "name": "Employee Training",
        "columns": [
            "Employee ID",
            "Employee Name",
            "Department",
            "Training Name",
            "Training Status",
            "Completion Date"
        ],
        "views": [
            "All Employees",
            "Department Employees"
        ]
    },

    "Document Library": {
        "name": "Training Documents",
        "folders": [
            "Training Materials",
            "Certificates",
            "Training Policies"
        ],
        "metadata": [
            "Document Type",
            "Department",
            "Training Name",
            "Document Status"
        ]
    },

    "Permissions": {
        "HR Manager": "Full Control",
        "Training Manager": "Edit",
        "Employee": "Read"
    }
}

print(sharepoint_structure)
