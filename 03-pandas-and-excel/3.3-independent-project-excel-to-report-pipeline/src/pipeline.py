import pandas as pd
def run_pipeline(input_file, output_file):
    df = pd.read_excel(input_file)
    errors = []

    # Validation
    for column in ["Name", "Age", "Salary"]:
        if column not in df.columns:
            errors.append(f"Missing column: {column}")

    if "Age" in df.columns:
        df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

    if "Salary" in df.columns:
        df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

    if df.isnull().any().any():
        errors.append("Missing or invalid values found")

    # Transformation
    if "Salary" in df.columns:
        df["Annual Salary"] = df["Salary"] * 12

    # Output workbook
    error_df = pd.DataFrame({"Errors": errors})

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Report", index=False)
        error_df.to_excel(writer, sheet_name="Error Summary", index=False)


run_pipeline("input.xlsx", "report.xlsx")
