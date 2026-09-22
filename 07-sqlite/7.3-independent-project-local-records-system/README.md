# Local Records System
## About
A simple student records system built using Python and SQLite.
The project stores student records and provides basic search, filtering, and reporting.

## Features
* Create database
* Add student records
* View records
* Search students
* Filter students by marks
* Generate a simple report
* Run basic tests
* Recover the database

## Technologies

* Python
* SQLite
* SQL

## Project Structure
7.3-independent-project-local-records-system/
│
├── data/
├── docs/
│   └── recovery.md
├── src/
│   ├── database.py
│   └── repository.py
├── tests/
│   └── test_repository.py
└── README.md

## How to Run
### 1. Initialize Database: python src/database.py
### 2. Run Project:python src/repository.py
### 3. Run Tests:python tests/test_repository.py

## Concepts Practiced
* SQLite
* SQL
* INSERT
* SELECT
* WHERE
* COUNT
* AVG
* Search
* Filtering
* Database persistence
* Testing
* Recovery

## Recovery
Delete `data/records.db` and run:python src/database.py
This creates a fresh database.

## Learning Outcome
This project helped me practice designing and implementing a small local persistence system independently.
