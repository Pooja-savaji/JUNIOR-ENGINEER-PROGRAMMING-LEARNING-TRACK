# Mini Order-Management Service (Phase 3 Independent Challenge)

A modular, domain-driven order management system demonstrating decoupled layered architecture, rich domain invariants, explicit state transitions, and test-driven development.

---

## 1. Architectural Defense & Design Rationale

### A. Separation of Concerns (Layered Architecture)
The service is divided into four distinct layers with unidirectional dependencies pointing inward:
1. **Domain Layer (`domain/`)**:
   - Contains pure business logic, entities (`Order`, `Customer`), value objects (`Money`, `OrderItem`), and domain errors.
   - Zero external framework or storage dependencies.
   - Enforces business invariants directly on domain objects (e.g. an order cannot be confirmed without items; an order cannot be modified once confirmed).
2. **Repository Layer (`repositories/`)**:
   - Defines formal generic contracts (`BaseRepository[T]`).
   - Completely decouples domain logic from persistence mechanisms.
   - Includes `MockRepository[T]` for unit testing without disk I/O or database dependencies, and `JsonFileRepository[T]` for file persistence.
3. **Service Layer (`services/`)**:
   - `OrderService` orchestrates user use cases (creating draft orders, checking out, applying tier-based discounts, calculating analytics).
   - Coordinates domain models and repositories without leaking database details into business rules.
4. **Presentation Layer (`cli/` & `main.py`)**:
   - Terminal interface for human interaction and automated demonstration mode (`--demo`).

### B. Value Object Semantics: Why `Money`?
Using native floating-point numbers for currency introduces rounding errors (e.g. `0.1 + 0.2 != 0.3`). The `Money` value object uses Python's `Decimal` with `ROUND_HALF_UP` quantization to guarantee exact currency arithmetic. In addition, `Money` encapsulates multi-currency safeguards—preventing accidental addition of different currencies (e.g. adding USD to EUR raises an immediate error).

### C. State Machine & Transition Invariants
The order lifecycle strictly transitions through a finite state machine:
```
           +-----------+
           |  PENDING  | (Items can be added/removed, discount/shipping set)
           +-----+-----+
                 | confirm() (Requires at least 1 item)
                 v
           +-----------+
           | CONFIRMED | (Items locked, waiting for settlement)
           +-----+-----+
                 | pay()
                 v
           +-----------+
           |   PAID    | (Ready for fulfillment)
           +-----+-----+
                 | ship(tracking_number)
                 v
           +-----------+
           |  SHIPPED  | (In transit)
           +-----+-----+
                 | deliver()
                 v
           +-----------+
           | DELIVERED | (Terminal state)
           +-----------+

Cancellation rule: cancel() is allowed ONLY from PENDING, CONFIRMED, or PAID.
Attempting to cancel an order that is SHIPPED or DELIVERED raises InvalidOrderStateError.
```

---

## 2. Directory Structure

```
02_oop_modular_design/independent/
├── order_service/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py            # Order, OrderItem, Customer, Money, Enums
│   │   └── exceptions.py        # OrderNotFoundError, InvalidOrderStateError, etc.
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py              # BaseRepository[T] ABC
│   │   ├── in_memory.py         # MockRepository[T] test double
│   │   └── json_file.py         # JsonFileRepository[T] atomic file persistence
│   ├── services/
│   │   ├── __init__.py
│   │   └── order_service.py     # Application business use cases & sales analytics
│   └── cli/
│       ├── __init__.py
│       └── cli_app.py           # Console interactive UI and --demo runner
├── data/                        # JSON storage (customers.json, orders.json)
├── tests/
│   └── test_order_service.py   # Unit test suite with mock repositories
├── main.py                      # Composition Root
└── README.md                    # Architecture defense & guide
```

---

## 3. How to Run

### Run Unit Tests
```bash
python -m unittest tests/test_order_service.py
```

### Run Automated End-to-End Walkthrough Demo
```bash
python main.py --demo
```

### Run Interactive Terminal Menu
```bash
python main.py
```
