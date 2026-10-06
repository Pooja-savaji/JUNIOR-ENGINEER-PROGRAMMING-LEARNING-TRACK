# Sharepoint Records Application

## Objective
Build a generic SharePoint-backed records application using a supplied schema.

## Task

- Implement CRUD operations for records.
- Add document upload and retrieval.
- Handle basic errors.
- Write tests for the application.

## Project Structure

```text
6.3-independent-project-sharepoint-records-application/
├── data/
│   └── records.json
├── docs/
│   └── schema.md
├── src/
│   └── sharepoint_records.py
├── tests/
│   └── test_sharepoint_records.py
└── README.md
```

## Features

- Create records
- Read records
- Update records
- Delete records
- Upload documents
- Retrieve documents
- Basic error handling
- Unit testing

## Run
1.python src/sharepoint_records.py

2.python -m unittest discover tests

## Pass Criteria
Can implement the SharePoint integration from documentation alone, including CRUD, document storage, error handling, and tests.
