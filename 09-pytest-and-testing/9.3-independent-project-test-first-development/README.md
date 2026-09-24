# 12.6 Independent Challenge – Test-First Development

## About
This project practices test-first development using a small Python module. The goal is to find a problem, write a test, fix the code, and keep the test to prevent the problem from happening again.

## Topics Covered
* Test-first development
* Writing tests before fixing code
* Debugging with tests
* Regression testing
* Validating expected behavior
* Using pytest

## What I Practiced
* Reviewed an existing piece of code.
* Identified an incorrect behavior.
* Wrote a test for the expected behavior.
* Ran the test to identify the problem.
* Fixed the code.
* Ran the tests again to verify the fix.
* Added regression coverage to prevent the same bug from returning.

## Project Structure
9.3-independent-project-test-first-development/
├── data/
│   └── sample_data.json
├── docs/
│   └── bug-notes.md
├── src/
│   └── discount.py
├── tests/
│   └── test_discount.py
└── README.md


## Testing

The project uses `pytest` to run the tests.
The tests cover:
* Normal discount
* Full discount
* Invalid discount
* Regression case

## Learning Goals
* Learn how tests can help find bugs.
* Learn how to write tests for expected behavior.
* Understand regression testing.
* Practice fixing code using test results.
* Use tests as a development and debugging tool.





