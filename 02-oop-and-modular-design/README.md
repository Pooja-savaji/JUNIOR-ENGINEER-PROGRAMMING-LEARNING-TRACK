# OOP & Modular Design

Object-oriented programming principles, classes, inheritance, encapsulation, abstract base classes, dunder methods, dataclasses, and modular architectural patterns.

## Included Learned Programs (`learned/`)
- `01_classes_and_encapsulation.py`: Bank account & digital wallet system demonstrating instance vs class attributes, `@property` getters/setters, state invariant validation, transaction history, atomic transfer rollbacks, and class-level reserve registries.
- `02_inheritance_and_polymorphism.py`: Corporate staff role hierarchy (`Employee`, `SoftwareEngineer`, `EngineeringManager`, `Contractor`) demonstrating `super().__init__()`, method overriding, composition over inheritance (managers holding direct reports), and polymorphic payroll dispatch.
- `03_abstract_interfaces.py`: Formal contracts using `abc.ABC` and `@abstractmethod`. Implements pluggable notification channels (`EmailNotifier`, `SMSNotifier`, `SlackWebhookNotifier`) and payment gateways (`StripePaymentGateway`, `PayPalPaymentGateway`, `MockPaymentGateway`) injected into an `OrderCheckoutService` following the Dependency Inversion Principle.
- `04_magic_dunder_methods.py`: Domain value object (`Money`) with exact decimal precision, string representations (`__repr__`, `__str__`), equality & hashing (`__eq__`, `__hash__`), arithmetic operator overloading (`+`, `-`, `*`, `/`), total ordering (`<`, `<=`), container protocol collection (`AssetPortfolio`), and context manager (`SafeTransactionScope`) for atomic rollback safety.
- `05_dataclasses_and_domain_models.py`: Enterprise asset models (`User`, `MaintenanceLog`, `HardwareAsset`) utilizing `@dataclass`, `frozen=True` immutability, `__post_init__` invariant validation, straight-line depreciation calculation, and bidirectional JSON serialization (`to_dict`, `from_dict`, `to_json`, `from_json`).

## Included Project-Ready Application (`project_ready/`)
- `asset_tracker/`: 4-tier layered enterprise IT Asset Management System:
  - `models/`: Domain hierarchy with `Asset` (ABC), `HardwareAsset`, `SoftwareLicense`, `Employee`, and `AssignmentRecord`.
  - `exceptions/`: Domain exception hierarchy (`AssetNotFoundError`, `AssetAlreadyAssignedError`, `LicenseSeatsExhaustedError`, etc.).
  - `repositories/`: Persistence abstraction with `BaseRepository[T]` ABC, `JsonRepository[T]` (atomic file persistence), and `InMemoryRepository[T]` (mock testing double).
  - `services/`: `AssetService` business orchestrator for deployments, straight-line inventory depreciation, and operational audit metrics.
  - `cli/`: `ConsoleApp` terminal presentation layer with interactive menu and `--demo` walkthrough runner.
  - `tests/`: Automated unit test suite with 100% passing tests for business logic, error conditions, and inventory valuations.

## Included Independent Application (`independent/`)
- `order_service/`: 4-tier domain-driven Mini Order-Management System:
  - `domain/`: Pure domain models (`Order`, `OrderItem`, `Customer`, `Money` value object with Decimal precision, `OrderStatus` FSM), and domain error hierarchy.
  - `repositories/`: `BaseRepository[T]` interface, `MockRepository[T]` for unit testing, and `JsonFileRepository[T]` for atomic file persistence.
  - `services/`: `OrderService` handling draft orders, tier-based discounts, state transitions, item adjustments, and sales analytics.
  - `cli/`: `OrderConsoleApp` terminal menu and `--demo` automated end-to-end runner.
  - `tests/`: Comprehensive unit test suite with 11 hermetic tests covering invariants, pricing, and lifecycle state rules.

## Progress

- [x] Learned
- [x] Project Ready
- [x] Independent


