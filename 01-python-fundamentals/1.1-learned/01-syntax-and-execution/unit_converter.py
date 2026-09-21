"""Multi-Category Unit Converter in Pure Python.

Covers: dictionaries, nested data structures, arithmetic transformations,
string formatting, error handling, and unit scaling factors.
"""

from typing import Dict, List, Optional, Tuple


# Length conversion factors to meters
LENGTH_FACTORS: Dict[str, float] = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "mi": 1609.344,
    "yd": 0.9144,
    "ft": 0.3048,
    "in": 0.0254,
}

# Mass/Weight conversion factors to kilograms
WEIGHT_FACTORS: Dict[str, float] = {
    "kg": 1.0,
    "g": 0.001,
    "mg": 0.000001,
    "lb": 0.45359237,
    "oz": 0.028349523125,
    "ton": 1000.0,
}

# Digital Storage conversion factors to Bytes
STORAGE_FACTORS: Dict[str, float] = {
    "B": 1.0,
    "KB": 1024.0,
    "MB": 1024.0**2,
    "GB": 1024.0**3,
    "TB": 1024.0**4,
    "PB": 1024.0**5,
}

# Speed conversion factors to meters per second
SPEED_FACTORS: Dict[str, float] = {
    "m/s": 1.0,
    "km/h": 1.0 / 3.6,
    "mph": 0.44704,
    "knot": 0.514444,
}


def convert_by_factor(
    value: float,
    from_unit: str,
    to_unit: str,
    factors: Dict[str, float],
) -> float:
    """Convert value using base unit factors."""
    from_key = from_unit.strip().lower()
    to_key = to_unit.strip().lower()

    # Case insensitive lookup
    factor_map = {k.lower(): v for k, v in factors.items()}
    if from_key not in factor_map:
        raise ValueError(f"Unknown source unit '{from_unit}'. Supported: {list(factors.keys())}")
    if to_key not in factor_map:
        raise ValueError(f"Unknown target unit '{to_unit}'. Supported: {list(factors.keys())}")

    base_value = value * factor_map[from_key]
    return base_value / factor_map[to_key]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between Celsius (C), Fahrenheit (F), and Kelvin (K)."""
    src = from_unit.strip().upper()
    dst = to_unit.strip().upper()

    # Convert source to Celsius first
    if src == "C":
        celsius = value
    elif src == "F":
        celsius = (value - 32) * 5 / 9
    elif src == "K":
        celsius = value - 273.15
    else:
        raise ValueError(f"Unknown temperature unit '{from_unit}'. Use C, F, or K.")

    # Convert Celsius to destination
    if dst == "C":
        return celsius
    elif dst == "F":
        return (celsius * 9 / 5) + 32
    elif dst == "K":
        return celsius + 273.15
    else:
        raise ValueError(f"Unknown temperature unit '{to_unit}'. Use C, F, or K.")


def run_unit_converter_cli():
    """Interactive CLI menu for unit conversions."""
    print("=" * 55)
    print("           📏 PYTHON UNIT CONVERTER                ")
    print("=" * 55)

    categories = [
        ("1", "Length", LENGTH_FACTORS, "m, km, cm, mm, mi, yd, ft, in"),
        ("2", "Weight / Mass", WEIGHT_FACTORS, "kg, g, mg, lb, oz, ton"),
        ("3", "Temperature", None, "C (Celsius), F (Fahrenheit), K (Kelvin)"),
        ("4", "Digital Storage", STORAGE_FACTORS, "B, KB, MB, GB, TB, PB"),
        ("5", "Speed", SPEED_FACTORS, "m/s, km/h, mph, knot"),
    ]

    while True:
        print("\nSelect Category:")
        for code, name, _, units in categories:
            print(f"  {code}. {name:<18} (Units: {units})")
        print("  0. Exit")

        choice = input("\nEnter category (0-5): ").strip()

        if choice == "0":
            print("\nThank you for using Unit Converter! Goodbye! 👋\n")
            break

        matched = [c for c in categories if c[0] == choice]
        if not matched:
            print("[Error] Invalid choice.")
            continue

        _, cat_name, factors, units_str = matched[0]

        try:
            val_str = input(f"\nEnter value to convert: ").strip()
            value = float(val_str)
            from_u = input(f"From unit ({units_str}): ").strip()
            to_u = input(f"To unit   ({units_str}): ").strip()

            if choice == "3":
                converted = convert_temperature(value, from_u, to_u)
            else:
                converted = convert_by_factor(value, from_u, to_u, factors)

            print("-" * 45)
            print(f"Result: {value:,.4f} {from_u} = {converted:,.4f} {to_u}")
            print("-" * 45)

        except ValueError as err:
            print(f"[Error] {err}")


if __name__ == "__main__":
    run_unit_converter_cli()
