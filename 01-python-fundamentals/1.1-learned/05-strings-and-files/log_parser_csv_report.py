"""
log_parser_csv_report.py
========================
Day 1 - Python Fundamentals Exercise
Parse a plain-text log file and generate two CSV reports:
  1. full_report.csv   -- every log entry (timestamp, level, message)
  2. summary_report.csv -- count and percentage per log level

Concepts used: file I/O, string methods, lists, dicts, csv module,
               functions, type hints, f-strings.

Run:
    python log_parser_csv_report.py
    python log_parser_csv_report.py --log myfile.log --filter ERROR
"""

import csv
import os
import argparse
from datetime import datetime


# ─────────────────────────────────────────────────────────────────────────────
# 1. DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────────────────
# We represent each log entry as a simple dictionary with three keys.
# Example: {"timestamp": "2024-01-15 08:00:01", "level": "INFO",
#           "message": "Application started"}

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


# ─────────────────────────────────────────────────────────────────────────────
# 2. PARSING FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def parse_line(line: str) -> dict | None:
    """Parse one log line and return a dict, or None if the line is invalid.

    Expected format:
        YYYY-MM-DD HH:MM:SS LEVEL  Message text here
    """
    line = line.strip()
    if not line:
        return None  # skip blank lines

    parts = line.split(None, 3)  # split on whitespace, max 4 parts
    # parts = ["2024-01-15", "08:00:01", "INFO", "Application started"]

    if len(parts) < 4:
        return None  # not enough fields, skip

    date_str, time_str, level, message = parts

    # Validate the level
    level = level.upper().strip()
    if level not in LOG_LEVELS:
        return None

    # Combine date and time
    timestamp = f"{date_str} {time_str}"

    return {
        "timestamp": timestamp,
        "level":     level,
        "message":   message.strip(),
    }


def parse_log_file(filepath: str) -> list:
    """Read a log file and return a list of parsed log entry dicts.

    Skips invalid or blank lines silently.
    """
    entries = []

    if not os.path.exists(filepath):
        print(f"ERROR: Log file not found: {filepath}")
        return entries

    with open(filepath, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            entry = parse_line(line)
            if entry:
                entries.append(entry)
            # If parse_line returns None we just skip that line

    print(f"Parsed {len(entries)} valid log entries from: {filepath}")
    return entries


# ─────────────────────────────────────────────────────────────────────────────
# 3. FILTER FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def filter_by_level(entries: list, level: str) -> list:
    """Return only entries whose level matches *level* (case-insensitive).

    Pass level='' or level=None to get all entries back unchanged.
    """
    if not level:
        return entries
    level = level.upper().strip()
    filtered = [e for e in entries if e["level"] == level]
    print(f"Filtered to {len(filtered)} entries with level: {level}")
    return filtered


# ─────────────────────────────────────────────────────────────────────────────
# 4. ANALYSIS FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def build_summary(entries: list) -> list:
    """Count entries per log level and calculate percentages.

    Returns a list of dicts:
    [{"level": "INFO", "count": 15, "percentage": "60.0%"}, ...]
    """
    # Step 1: count each level
    counts = {}
    for entry in entries:
        level = entry["level"]
        counts[level] = counts.get(level, 0) + 1

    total = len(entries)

    # Step 2: build summary rows in a fixed order
    summary = []
    for level in LOG_LEVELS:
        count = counts.get(level, 0)
        percentage = (count / total * 100) if total > 0 else 0
        summary.append({
            "level":      level,
            "count":      count,
            "percentage": f"{percentage:.1f}%",
        })

    return summary


# ─────────────────────────────────────────────────────────────────────────────
# 5. CSV REPORT WRITERS
# ─────────────────────────────────────────────────────────────────────────────

def write_full_report(entries: list, output_path: str) -> None:
    """Write all log entries to a CSV file.

    Columns: timestamp, level, message
    """
    fieldnames = ["timestamp", "level", "message"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()         # writes the column names row
        writer.writerows(entries)    # writes all data rows at once

    print(f"Full report saved: {output_path}  ({len(entries)} rows)")


def write_summary_report(summary: list, output_path: str) -> None:
    """Write the level-count-percentage summary to a CSV file.

    Columns: level, count, percentage
    """
    fieldnames = ["level", "count", "percentage"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary)

    print(f"Summary report saved: {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# 6. DISPLAY HELPERS  (print results to the terminal)
# ─────────────────────────────────────────────────────────────────────────────

def print_summary_table(summary: list) -> None:
    """Print the summary as a formatted table in the terminal."""
    print()
    print("=" * 44)
    print("  LOG LEVEL SUMMARY")
    print("=" * 44)
    print(f"  {'Level':<12} {'Count':>6}  {'Percentage':>10}")
    print("-" * 44)
    for row in summary:
        print(f"  {row['level']:<12} {row['count']:>6}  {row['percentage']:>10}")
    print("=" * 44)


def print_entries_table(entries: list, max_rows: int = 10) -> None:
    """Print up to *max_rows* entries as a table in the terminal."""
    print()
    print("=" * 70)
    print("  LOG ENTRIES (first", min(max_rows, len(entries)), "shown)")
    print("=" * 70)
    print(f"  {'Timestamp':<20} {'Level':<10} {'Message'}")
    print("-" * 70)
    for entry in entries[:max_rows]:
        msg = entry["message"][:38] + "..." if len(entry["message"]) > 40 else entry["message"]
        print(f"  {entry['timestamp']:<20} {entry['level']:<10} {msg}")
    if len(entries) > max_rows:
        print(f"  ... and {len(entries) - max_rows} more rows (see CSV)")
    print("=" * 70)


# ─────────────────────────────────────────────────────────────────────────────
# 7. MAIN — ties everything together
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # --- argument parsing ---------------------------------------------------
    parser = argparse.ArgumentParser(
        description="Parse a log file and generate CSV reports."
    )
    parser.add_argument(
        "--log",
        default="sample_app.log",
        help="Path to the log file  (default: sample_app.log)",
    )
    parser.add_argument(
        "--filter",
        default="",
        help="Only include this log level  (e.g. ERROR, WARNING)",
    )
    parser.add_argument(
        "--out-dir",
        default=".",
        help="Directory to save CSV reports  (default: current folder)",
    )
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    print()
    print("=" * 50)
    print("  LOG PARSER & CSV REPORT GENERATOR")
    print("=" * 50)

    # Step 1: Parse
    all_entries = parse_log_file(args.log)
    if not all_entries:
        print("No entries to process. Exiting.")
        return

    # Step 2: (optional) filter
    entries = filter_by_level(all_entries, args.filter)

    # Step 3: Analyse
    summary = build_summary(entries)

    # Step 4: Show on screen
    print_summary_table(summary)
    print_entries_table(entries)

    # Step 5: Write CSV reports
    full_path    = os.path.join(args.out_dir, "full_report.csv")
    summary_path = os.path.join(args.out_dir, "summary_report.csv")

    write_full_report(entries, full_path)
    write_summary_report(summary, summary_path)

    print()
    print("Done! Open the CSV files in Excel or any spreadsheet app.")


if __name__ == "__main__":
    main()
