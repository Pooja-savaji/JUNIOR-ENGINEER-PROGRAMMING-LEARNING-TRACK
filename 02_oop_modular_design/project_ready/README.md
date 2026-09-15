# Modular IT Asset Management System (Phase 2)

A modular, enterprise-grade Python application demonstrating object-oriented programming (OOP), domain-driven design, and layered architecture.

---

## 1. Architectural Overview

The application follows a **4-tier layered architecture** ensuring high cohesion and loose coupling:

02_oop_modular_design/project_ready/
├── asset_tracker/
│   ├── __init__.py
│   ├── models/                  # Tier 1: Domain Entities & Value Objects
│   │   ├── __init__.py
│   │   ├── asset.py             # Base Asset (ABC), HardwareAsset, SoftwareLicense
│   │   ├── employee.py          # Employee entity with email validation
│   │   └── assignment.py        # Checkout/Checkin assignment record
│   ├── exceptions/              # Domain-Specific Error Hierarchy
│   │   ├── __init__.py
│   │   └── errors.py            # AssetNotFoundError, AssetAlreadyAssignedError, etc.
│   ├── repositories/            # Tier 2: Persistence Layer (Generic CRUD Contracts)
│   │   ├── __init__.py
│   │   ├── base.py              # BaseRepository[T] ABC
│   │   └── json_repo.py         # JsonRepository[T] (file-backed) & InMemoryRepository[T] (test double)
│   ├── services/                # Tier 3: Business Logic & Orchestration
│   │   ├── __init__.py
│   │   └── asset_service.py     # Check-out, check-in, straight-line depreciation, audit reports
│   └── cli/                     # Tier 4: Presentation Layer
│       ├── __init__.py
│       └── console_app.py       # Terminal interactive UI and automated demo runner
├── data/                        # JSON storage directory (auto-seeded on first run)
├── main.py                      # Composition Root & Dependency Injection
└── tests/
    └── test_asset_service.py   # Unit test suite using fast InMemoryRepository doubles

---

## 2. Key OOP & Design Patterns Employed

- **Abstract Base Classes (bc.ABC)**:
  - Asset: Formal root interface requiring calculate_current_value() and serialization methods.
  - BaseRepository[T]: Generic collection-oriented CRUD contract.
- **Polymorphism & Subtyping**:
  - HardwareAsset: Serial numbers, warranty tracking, and straight-line depreciation across useful lifespan.
  - SoftwareLicense: Seat allocation tracking, key management, and subscription amortization.
- **Encapsulation & Invariants**:
  - Double checkout prevention (AssetAlreadyAssignedError).
  - License seat exhaustion safeguards (LicenseSeatsExhaustedError).
  - Maintenance and retirement lifecycle state guards.
- **Dependency Inversion**:
  - AssetService depends only on BaseRepository[T] interfaces, allowing trivial swapping between file-backed JSON storage and in-memory mock repositories.

---

## 3. Running the Application

### Automated Walkthrough Demo
Run the automated end-to-end lifecycle demonstration:
ash
python main.py --demo

### Interactive Console CLI
Launch the interactive terminal menu:
ash
python main.py

### Running Unit Tests
Execute the unit test suite:
ash
python -m unittest tests/test_asset_service.py
