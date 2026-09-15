# OOP & Modular Design

Object-oriented programming principles, classes, inheritance, encapsulation, abstract base classes, dunder methods, dataclasses, and modular architectural patterns.

## Included Learned Programs (`learned/`)
- `01_classes_and_encapsulation.py`: Bank account & digital wallet system demonstrating instance vs class attributes, `@property` getters/setters, state invariant validation, transaction history, atomic transfer rollbacks, and class-level reserve registries.
- `02_inheritance_and_polymorphism.py`: Corporate staff role hierarchy (`Employee`, `SoftwareEngineer`, `EngineeringManager`, `Contractor`) demonstrating `super().__init__()`, method overriding, composition over inheritance (managers holding direct reports), and polymorphic payroll dispatch.
- `03_abstract_interfaces.py`: Formal contracts using `abc.ABC` and `@abstractmethod`. Implements pluggable notification channels (`EmailNotifier`, `SMSNotifier`, `SlackWebhookNotifier`) and payment gateways (`StripePaymentGateway`, `PayPalPaymentGateway`, `MockPaymentGateway`) injected into an `OrderCheckoutService` following the Dependency Inversion Principle.
- `04_magic_dunder_methods.py`: Domain value object (`Money`) with exact decimal precision, string representations (`__repr__`, `__str__`), equality & hashing (`__eq__`, `__hash__`), arithmetic operator overloading (`+`, `-`, `*`, `/`), total ordering (`<`, `<=`), container protocol collection (`AssetPortfolio`), and context manager (`SafeTransactionScope`) for atomic rollback safety.
- `05_dataclasses_and_domain_models.py`: Enterprise asset models (`User`, `MaintenanceLog`, `HardwareAsset`) utilizing `@dataclass`, `frozen=True` immutability, `__post_init__` invariant validation, straight-line depreciation calculation, and bidirectional JSON serialization (`to_dict`, `from_dict`, `to_json`, `from_json`).

## Progress

- [x] Learned
- [ ] Project Ready
- [ ] Independent

