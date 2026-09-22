# Excel-to-Report Pipeline
 1.Overview
This project is a reusable Excel-to-Report data pipeline built using Python, Pandas, and OpenPyXL.
The pipeline reads employee data from an Excel file, validates the data, performs transformations, and generates a final Excel report with an error summary.

2.Project Structure
3.3-independent-project-excel-to-report-pipeline/
│
├── data/
│   └── input.xlsx
│
├── docs/
│   └── assumptions.md
│
├── src/
│   └── pipeline.py
│
├── tests/
│   └── test_pipeline.py
│
└── README.md

 3.Technologies Used

* Python
* Pandas
* OpenPyXL
* Excel
* Pytest

4.Input Data
The input Excel file contains employee information.
Required columns:
* Name
* Age
* Salary

Example:

| Name  | Age | Salary |
| ----- | --: | -----: |
| Pooja |  21 |  30000 |
| Rahul |  22 |  35000 |
| Sneha |  21 |  32000 |

 5.Pipeline Workflow

Excel Input
     ↓
Read Excel File
     ↓
Validate Data
     ↓
Clean and Convert Data
     ↓
Transform Data
     ↓
Generate Report
     ↓
Generate Error Summary


6. Validation
The pipeline checks:
* Required columns
* Missing values
* Valid age values
* Valid salary values
* Invalid data

 7.Data Transformation
The pipeline calculates annual salary using:
Annual Salary = Monthly Salary × 12


8. Output
The pipeline generates an Excel report containing two sheets.

 A.Report Sheet
Contains the processed employee data.

| Name  | Age | Salary | Annual Salary |
| ----- | --: | -----: | ------------: |
| Pooja |  21 |  30000 |        360000 |
| Rahul |  22 |  35000 |        420000 |
| Sneha |  21 |  32000 |        384000 |

 B.Error Summary Sheet

Contains errors found during validation.
Example:

| Errors                 |
| ---------------------- |
| Missing column: Salary |
| Invalid age found      |

9.Assumptions
Project assumptions are documented in:docs/assumptions.md
Main assumptions:
* Name, Age, and Salary are required columns.
* Age must be a valid number.
* Salary must be greater than 0.
* Missing or invalid values should be reported.
* Annual Salary is calculated using Monthly Salary × 12.
* The original input file is not modified.

 10.Testing
Tests are available in:tests/test_pipeline.py
Run the tests using:pytest

11.How to Run
 1. Install dependencies: pip install pandas openpyxl pytest
 2. Add the input file- Place the Excel file inside:data/input.xlsx
 3. Run the pipeline:python src/pipeline.py
 4. Check the output-The generated report will be created as:data/report.xlsx

12.Project Goal
The goal of this project is to demonstrate the ability to independently build a small and reusable Excel data-processing pipeline.
This project covers:
* Excel data handling
* Data validation
* Data cleaning
* Data transformation
* Error handling
* Excel report generation
* Testing
* Documentation


