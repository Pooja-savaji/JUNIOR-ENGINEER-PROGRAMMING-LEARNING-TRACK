# Day 1 Independent Challenge: CLI Expense Tracker

A lightweight, robust command-line expense tracker built entirely using **Python fundamentals** (no external libraries or frameworks).

## Features
- **Add Expenses**: Record transactions with description, positive amount, category, date, and optional notes.
- **List Expenses**: Formatted, aligned table showing ID, date, category, amount, and description.
- **Summary & Breakdown**: Real-time grand total and percentage distribution across spending categories.
- **Category Filtering**: Filter transactions by standard categories (Food, Travel, Equipment, Software, etc.).
- **Delete Record**: Safe removal by transaction ID.
- **Persistence**: Automatically reads and writes records to `expenses.json` using standard library `json`.

## Edge Cases Handled
- **Non-numeric & Negative Amounts**: Validates user input and rejects negative numbers or non-numeric strings with helpful prompts.
- **Empty Descriptions**: Prevents saving blank descriptions.
- **Date Validation**: Validates `YYYY-MM-DD` format and defaults to today's date if left blank.
- **Missing / Corrupted File**: Gracefully recovers if `expenses.json` is missing or corrupted.
- **Zero Division**: Category breakdown handles zero total gracefully.

## How to Run

### Interactive Menu:
```bash
python main.py
```

### Quick Commands:
```bash
python main.py list
python main.py summary
```
