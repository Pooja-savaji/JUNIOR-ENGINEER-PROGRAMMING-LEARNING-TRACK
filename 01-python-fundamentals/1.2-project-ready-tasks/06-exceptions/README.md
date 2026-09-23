# 4.6 Exceptions

## Overview
Exceptions are errors that occur while a Python program is running. Exception handling allows a program to handle expected errors without stopping unexpectedly.

## Topics Covered

### 1. try
The `try` block contains code that may cause an exception. Python checks this block for errors while the program is running.

### 2. except
The `except` block handles an exception when an error occurs in the `try` block. It allows the program to respond to expected errors.

### 3. else
The `else` block runs when no exception occurs in the `try` block. It is used for code that should run only when the operation is successful.

### 4. finally
The `finally` block runs whether an exception occurs or not. It is commonly used for cleanup operations.

### 5. Raising Exceptions
Raising an exception means intentionally generating an error when a specific condition is not valid or cannot be accepted.

### 6. Custom Exceptions
Custom exceptions are user-defined exception types created for specific situations in an application. They make error handling more meaningful and easier to understand.

### 7. Validation
Validation checks whether input or data meets the required rules before it is processed.
Good validation helps prevent invalid data from entering the program and allows expected input errors to be handled properly.

## Exception Handling Flow
Python exception handling generally follows this structure:
* `try` — Code that may cause an error.
* `except` — Handles the error.
* `else` — Runs when there is no error.
* `finally` — Runs whether there is an error or not.

## Learning Outcome
After completing this section, I understand how Python exceptions work and how to handle expected errors using `try`, `except`, `else`, and `finally`. I can also raise exceptions, create custom exceptions, and validate input before processing it.
