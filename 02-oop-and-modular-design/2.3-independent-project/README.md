# Mini Order Management Service
A simple Python service for creating and managing orders.

## Features
* Create order
* Cancel order
* Validate customer
* Validate amount
* Store orders
* Unit testing

## Architecture
Order
  ↓
Service
  ↓
Repository

## Project Structure
src/
├── order.py
├── service.py
└── repository.py

tests/
└── test_order.py

README.md
requirements.txt

## Run
Install dependencies: pip install -r requirements.txt
Run tests:pytest

## Validation
* Customer cannot be empty.
* Amount must be greater than 0.
* Order must exist before cancellation.

## Learning
This project demonstrates:
* Domain model
* Service layer
* Repository layer
* Validation
* Testing
* Exception handling

