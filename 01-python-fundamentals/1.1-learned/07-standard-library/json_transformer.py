"""
json_transformer.py
====================
Day 1 - Python Fundamentals Exercise
Topic  : Reshape, filter, and transform JSON data

Features
--------
1.  load_json(path)             - read JSON from file
2.  save_json(data, path)       - write JSON to file
3.  filter_records(records, **conditions) - filter list by field values
4.  pick_fields(records, fields)- keep only named columns
5.  rename_keys(records, mapping) - rename field names
6.  add_computed_field(records, name, fn) - add a derived column
7.  group_by(records, key)      - group list into dict-of-lists
8.  flatten_record(record)      - nested dict -> flat dict
9.  sort_records(records, key, reverse) - sort list by field
10. summarise(records, group_key, value_key) - aggregate totals

Run:
    python json_transformer.py
"""

import json
import os
from copy import deepcopy


# ─────────────────────────────────────────────────────────────────────────────
# CORE I/O
# ─────────────────────────────────────────────────────────────────────────────

def load_json(path: str) -> dict | list:
    """Load and return parsed JSON from *path*."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path: str, indent: int = 2) -> None:
    """Serialise *data* to JSON and write to *path*."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    print(f"  Saved: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# TRANSFORMATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def filter_records(records: list, **conditions) -> list:
    """Keep only records where every keyword matches.

    Supports exact match and special suffixes:
      field=value        -> exact equality
      field__gt=value    -> greater than
      field__lt=value    -> less than
      field__contains=v  -> substring / list membership

    Example:
        filter_records(employees, department="Engineering", active=True)
        filter_records(employees, salary__gt=70000)
    """
    result = []
    for record in records:
        match = True
        for condition, expected in conditions.items():
            if "__" in condition:
                field, op = condition.rsplit("__", 1)
            else:
                field, op = condition, "eq"

            actual = record.get(field)

            if op == "eq" and actual != expected:
                match = False
            elif op == "gt" and not (actual is not None and actual > expected):
                match = False
            elif op == "lt" and not (actual is not None and actual < expected):
                match = False
            elif op == "contains":
                if isinstance(actual, list) and expected not in actual:
                    match = False
                elif isinstance(actual, str) and expected not in actual:
                    match = False

            if not match:
                break
        if match:
            result.append(record)
    return result


def pick_fields(records: list, fields: list) -> list:
    """Return records containing only the specified *fields*.

    Example:
        pick_fields(employees, ["id", "name", "salary"])
    """
    return [{k: r[k] for k in fields if k in r} for r in records]


def rename_keys(records: list, mapping: dict) -> list:
    """Rename fields in every record according to *mapping* {old: new}.

    Example:
        rename_keys(records, {"name": "full_name", "salary": "annual_pay"})
    """
    result = []
    for record in records:
        new_record = {}
        for k, v in record.items():
            new_key = mapping.get(k, k)   # use mapping, or keep original
            new_record[new_key] = v
        result.append(new_record)
    return result


def add_computed_field(records: list, name: str, fn) -> list:
    """Add a new field *name* to every record, computed by calling fn(record).

    Example:
        add_computed_field(employees, "bonus",
                           lambda r: round(r["salary"] * 0.10, 2))
    """
    result = deepcopy(records)
    for record in result:
        record[name] = fn(record)
    return result


def group_by(records: list, key: str) -> dict:
    """Group records into a dict keyed by the value of *key*.

    Example:
        group_by(employees, "department")
        # -> {"Engineering": [...], "Sales": [...], ...}
    """
    groups: dict = {}
    for record in records:
        k = record.get(key, "unknown")
        groups.setdefault(k, []).append(record)
    return groups


def flatten_record(record: dict, parent_key: str = "",
                   separator: str = ".") -> dict:
    """Flatten a nested dict into a single-level dict with dotted keys.

    Example:
        flatten_record({"a": {"b": 1, "c": 2}})
        # -> {"a.b": 1, "a.c": 2}
    """
    items = {}
    for k, v in record.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_record(v, new_key, separator))
        else:
            items[new_key] = v
    return items


def sort_records(records: list, key: str,
                 reverse: bool = False) -> list:
    """Return records sorted by *key* (ascending by default).

    Example:
        sort_records(employees, "salary", reverse=True)
    """
    return sorted(records, key=lambda r: r.get(key) or 0, reverse=reverse)


def summarise(records: list, group_key: str, value_key: str) -> list:
    """Aggregate *value_key* totals per unique *group_key*.

    Returns a sorted list of dicts: {group_key: x, "total": y, "count": z,
                                     "average": w}
    """
    groups = group_by(records, group_key)
    summary = []
    for group, members in groups.items():
        values = [m.get(value_key, 0) for m in members
                  if m.get(value_key) is not None]
        total   = sum(values)
        count   = len(values)
        average = round(total / count, 2) if count else 0
        summary.append({
            group_key: group,
            "total":   total,
            "count":   count,
            "average": average,
        })
    return sort_records(summary, "total", reverse=True)


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

def section(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def pprint_list(records: list, max_rows: int = 5) -> None:
    """Pretty-print a list of dicts (first max_rows rows)."""
    for i, r in enumerate(records[:max_rows]):
        print(f"  {r}")
    if len(records) > max_rows:
        print(f"  ... and {len(records) - max_rows} more")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(script_dir, "sample_data.json")
    if not os.path.exists(data_file):
        data_file = "sample_data.json"
    if not os.path.exists(data_file):
        print(f"ERROR: 'sample_data.json' not found.")
        return

    print("=" * 60)
    print("  JSON TRANSFORMER")
    print("=" * 60)

    # Load
    data      = load_json(data_file)
    employees = data["employees"]
    print(f"  Loaded {len(employees)} employee records from {data_file!r}")

    # 1. Filter
    section("filter_records  — active Engineering staff")
    eng = filter_records(employees, department="Engineering", active=True)
    pprint_list(pick_fields(eng, ["id", "name", "salary"]))

    section("filter_records  — salary > 70 000")
    high_pay = filter_records(employees, salary__gt=70000)
    pprint_list(pick_fields(high_pay, ["name", "department", "salary"]))

    section("filter_records  — skill contains Python")
    pythonistas = filter_records(employees, skills__contains="Python")
    for e in pythonistas:
        print(f"  {e['name']:<15}  skills: {e['skills']}")

    # 2. Pick fields
    section("pick_fields  — id, name, email only")
    slim = pick_fields(employees, ["id", "name", "email"])
    pprint_list(slim)

    # 3. Rename keys
    section("rename_keys  — salary -> annual_pay, name -> full_name")
    renamed = rename_keys(employees[:3], {"salary": "annual_pay",
                                          "name": "full_name"})
    pprint_list(pick_fields(renamed, ["id", "full_name", "annual_pay"]))

    # 4. Add computed field
    section("add_computed_field  — bonus = 10% of salary")
    with_bonus = add_computed_field(employees,
                                    "bonus",
                                    lambda r: round(r["salary"] * 0.10, 2))
    pprint_list(pick_fields(with_bonus, ["name", "salary", "bonus"]))

    # 5. Group by
    section("group_by  — department")
    groups = group_by(employees, "department")
    for dept, members in groups.items():
        names = [m["name"] for m in members]
        print(f"  {dept:<15}: {names}")

    # 6. Sort
    section("sort_records  — salary descending")
    top = sort_records(employees, "salary", reverse=True)
    pprint_list(pick_fields(top, ["name", "department", "salary"]))

    # 7. Summarise
    section("summarise  — salary totals by department")
    dept_summary = summarise(employees, "department", "salary")
    print(f"  {'Department':<15} {'Total':>10}  {'Count':>5}  {'Average':>10}")
    print(f"  {'-'*45}")
    for row in dept_summary:
        print(f"  {row['department']:<15} {row['total']:>10,}  "
              f"{row['count']:>5}  {row['average']:>10,.2f}")

    # 8. Save a transformed output
    section("save_json  — active employees with bonus field")
    active = filter_records(employees, active=True)
    active_with_bonus = add_computed_field(active, "bonus",
                                           lambda r: round(r["salary"] * 0.10))
    out_file = os.path.join(script_dir, "active_employees_transformed.json")
    save_json(active_with_bonus, out_file)

    print()
    print("All JSON transformations complete!")


if __name__ == "__main__":
    main()
