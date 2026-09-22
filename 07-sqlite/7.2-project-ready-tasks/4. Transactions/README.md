# Task 10.4 — Transactions

## About
This task practices database transactions using Python and SQLite.
The main goal is to make sure related database operations are completed together and to prevent partial updates when an error occurs.

## Concepts Covered

* **Commit** — Saves database changes permanently.
* **Rollback** — Cancels changes when an error occurs.
* **Atomic Operation** — All related operations succeed or none are applied.
* **Failure Handling** — Handles errors safely using rollback.
* **Transaction** — Groups multiple database operations into one unit.

## Task

Build a simple **money transfer transaction**.
The program should:
1. Create two accounts.
2. Transfer money from one account to another.
3. Use `commit()` when the transfer succeeds.
4. Use `rollback()` when an error occurs.
5. Prevent partial updates.

## Files
* `transaction.py` — Contains the transaction exercise.

## What I Practiced
* Using `commit()`
* Using `rollback()`
* Handling database errors
* Understanding atomic operations
* Preventing partial database updates


