# CLI Expense Tracker
A simple Python command-line expense tracker for adding expenses, validating data, calculating totals, and generating category summaries.

## Features
* Add new expenses
* Validate expense amounts
* Calculate total expenses
* Generate category-wise summaries
* Store expense data in CSV format
* Import and export expense data
* Handle invalid input safely
* Run automated tests

## Project Structure
4.8-independent-challenge/
│
├── data/
│   └── expenses.csv
│
├── docs/
│   └── assumptions.md
│
├── src/
│   └── tracker.py
│
├── tests/
│   └── test_tracker.py
│
├── README.md
└── requirements.txt

## Technologies
* Python
* CSV
* Pytest

## Requirements
* Python 3.x
* Pytest

## Installation
Install the required package: pip install -r requirements.txt

## Running the Project
Run the tracker from the project folder: python src/tracker.py

## Running Tests
Run all tests using: pytest

## Validation Rules
The project checks that:
* Expense amount is greater than 0.
* Invalid amounts are rejected.
* Expense data follows the expected structure.
* Invalid input does not crash the program.

## Learning Outcomes
This project demonstrates:
* Functions
* Lists and dictionaries
* Input validation
* File handling
* CSV processing
* Exception handling
* Unit testing
* Basic project structure

## Independent Challenge
This project was completed as an independent challenge without step-by-step implementation instructions.
The project includes:
* A working expense tracker
* Tests
* README documentation
* Validation and edge-case handling
* CSV import/export
* A deliberately introduced defect that was identified and fixed
