# Recovery Instructions

## Initialize Database
Open the project terminal and run:python src/database.py
This creates the SQLite database and `students` table.

## Run the Project
python src/repository.py

## Run Tests
python tests/test_repository.py

## Recovery
If the database has a problem:
1. Delete `data/records.db`
2. Run:python src/database.py
The database will be created again.
