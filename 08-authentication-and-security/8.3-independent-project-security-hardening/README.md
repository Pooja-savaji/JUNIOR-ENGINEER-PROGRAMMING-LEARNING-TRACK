# Security Hardening

## About
This project focuses on identifying and fixing common security issues in a small application.

## What I Did
- Used password hashing for secure password storage.
- Added login verification.
- Added role-based access for admin users.
- Added tests for login and access control.

## Findings and Fixes

- **Plaintext password** → Used password hashing.
- **Unauthorized access** → Added role checking.
- **Invalid login** → Added password verification.

## Tests
Tests check that:
- Correct passwords allow login.
- Wrong passwords are rejected.
- Admin users get admin access.
- Normal users are denied admin access.

## Learning Outcome
I can identify and fix common security issues and write simple tests to check that the fixes work.
