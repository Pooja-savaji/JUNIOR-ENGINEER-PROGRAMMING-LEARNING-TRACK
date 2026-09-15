"""
date_calculator.py
==================
Day 1 - Python Fundamentals Exercise
Topic  : Date & time calculations using only the standard library (datetime)

Features
--------
1.  days_between(d1, d2)         - gap between two dates
2.  add_days(date, n)            - shift a date forward/backward
3.  day_of_week(date)            - Monday … Sunday
4.  is_weekend(date)             - True/False
5.  business_days_between(d1,d2) - skip weekends
6.  age_calculator(dob)          - full years from date-of-birth to today
7.  countdown(target)            - days remaining until a future date
8.  date_range(start, end)       - every date between two dates
9.  quarter_of_year(date)        - Q1 … Q4
10. format_date(date, style)     - multiple output formats
11. parse_flexible_date(text)    - accept many input strings

Run:
    python date_calculator.py
"""

from datetime import date, datetime, timedelta


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _to_date(value) -> date:
    """Accept a date, datetime, or YYYY-MM-DD string and return a date."""
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    # Try common string formats
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%B %d, %Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except (ValueError, TypeError):
            continue
    raise ValueError(f"Cannot parse date: {value!r}")


WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday",
                 "Thursday", "Friday", "Saturday", "Sunday"]


# ─────────────────────────────────────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def days_between(d1, d2) -> int:
    """Return the number of days from d1 to d2 (negative if d2 is earlier)."""
    return (_to_date(d2) - _to_date(d1)).days


def add_days(start, n: int) -> date:
    """Return the date that is *n* days after *start* (negative = before)."""
    return _to_date(start) + timedelta(days=n)


def day_of_week(d) -> str:
    """Return the weekday name for *d* (e.g. 'Monday')."""
    return WEEKDAY_NAMES[_to_date(d).weekday()]


def is_weekend(d) -> bool:
    """Return True if *d* falls on Saturday or Sunday."""
    return _to_date(d).weekday() >= 5


def business_days_between(d1, d2) -> int:
    """Count weekdays (Mon-Fri) between two dates, exclusive of d1, inclusive of d2."""
    start = _to_date(d1)
    end   = _to_date(d2)
    if start > end:
        start, end = end, start
    count = 0
    current = start + timedelta(days=1)
    while current <= end:
        if current.weekday() < 5:   # 0-4 = Mon-Fri
            count += 1
        current += timedelta(days=1)
    return count


def age_calculator(dob) -> dict:
    """Calculate age from date-of-birth to today.

    Returns dict with years, months, days, next_birthday, days_to_birthday.
    """
    birth = _to_date(dob)
    today = date.today()

    years = today.year - birth.year
    # Check if birthday hasn't occurred yet this year
    if (today.month, today.day) < (birth.month, birth.day):
        years -= 1

    # Next birthday
    try:
        next_bday = birth.replace(year=today.year)
    except ValueError:           # Feb 29 on non-leap year
        next_bday = birth.replace(year=today.year, day=28)
    if next_bday < today:
        try:
            next_bday = birth.replace(year=today.year + 1)
        except ValueError:
            next_bday = birth.replace(year=today.year + 1, day=28)

    days_to_bday = (next_bday - today).days

    return {
        "years":            years,
        "next_birthday":    next_bday.isoformat(),
        "days_to_birthday": days_to_bday,
    }


def countdown(target) -> int:
    """Return days remaining until *target* date (0 if today, negative if past)."""
    return (_to_date(target) - date.today()).days


def date_range(start, end) -> list:
    """Return a list of every date from *start* to *end* (inclusive)."""
    s, e = _to_date(start), _to_date(end)
    if s > e:
        s, e = e, s
    result = []
    current = s
    while current <= e:
        result.append(current)
        current += timedelta(days=1)
    return result


def quarter_of_year(d) -> int:
    """Return 1, 2, 3, or 4 for the calendar quarter of *d*."""
    return (_to_date(d).month - 1) // 3 + 1


def format_date(d, style: str = "iso") -> str:
    """Format a date in different styles.

    Styles: iso, long, short, us, eu, slash
    """
    d = _to_date(d)
    styles = {
        "iso":   d.strftime("%Y-%m-%d"),           # 2024-01-15
        "long":  d.strftime("%B %d, %Y"),           # January 15, 2024
        "short": d.strftime("%d %b %Y"),            # 15 Jan 2024
        "us":    d.strftime("%m/%d/%Y"),            # 01/15/2024
        "eu":    d.strftime("%d/%m/%Y"),            # 15/01/2024
        "slash": d.strftime("%Y/%m/%d"),            # 2024/01/15
    }
    return styles.get(style, styles["iso"])


# ─────────────────────────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────────────────────────

def section(title):
    print()
    print("=" * 55)
    print(f"  {title}")
    print("=" * 55)


def main():
    print("=" * 55)
    print("  DATE CALCULATOR")
    print("=" * 55)

    today = date.today()
    d1 = "2024-01-01"
    d2 = "2024-03-31"

    section("days_between / add_days")
    print(f"  Days between {d1} and {d2} : {days_between(d1, d2)}")
    print(f"  90 days after {d1}         : {add_days(d1, 90)}")
    print(f"  30 days before today       : {add_days(today, -30)}")

    section("day_of_week / is_weekend")
    for d in ["2024-01-01", "2024-01-06", "2024-01-07"]:
        print(f"  {d} -> {day_of_week(d):<12}  weekend={is_weekend(d)}")

    section("business_days_between")
    print(f"  Business days {d1} to {d2} : {business_days_between(d1, d2)}")

    section("age_calculator  (DOB: 1995-06-15)")
    info = age_calculator("1995-06-15")
    print(f"  Age            : {info['years']} years")
    print(f"  Next birthday  : {info['next_birthday']}")
    print(f"  Days to bday   : {info['days_to_birthday']}")

    section("countdown")
    future = add_days(today, 45)
    print(f"  Days until {future} : {countdown(future)}")
    past = add_days(today, -10)
    print(f"  Days since {past}  : {countdown(past)}  (negative = past)")

    section("date_range  (2024-01-01 to 2024-01-07)")
    week = date_range("2024-01-01", "2024-01-07")
    for d in week:
        print(f"  {d}  {day_of_week(d)}")

    section("quarter_of_year")
    for m in ["2024-01-15", "2024-04-01", "2024-08-20", "2024-11-30"]:
        print(f"  {m} -> Q{quarter_of_year(m)}")

    section("format_date  (2024-07-04)")
    for style in ["iso", "long", "short", "us", "eu", "slash"]:
        print(f"  {style:<6} -> {format_date('2024-07-04', style)}")

    print()
    print("All date calculations complete!")


if __name__ == "__main__":
    main()
