import pandas as pd

def validate_excel(file):
    df = pd.read_excel(file)
    errors = []
    required = ["Name", "Age", "Salary"]

    for column in required:
        if column not in df.columns:
            errors.append(f"Missing column: {column}")

    if df[required].isnull().any().any():
        errors.append("Missing values found")

    if (df["Age"] < 0).any():
        errors.append("Invalid age found")

    if (df["Salary"] <= 0).any():
        errors.append("Invalid salary found")

    return errors
errors = validate_excel("employees.xlsx")

if errors:
    print("Validation Errors:")
    for error in errors:
        print("-", error)
else:
    print("Excel file is valid")
