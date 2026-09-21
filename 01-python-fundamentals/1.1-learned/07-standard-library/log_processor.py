"""
log_processor.py
================
Day 1 - Python Fundamentals Exercise
Topic  : Advanced log processing — parse, analyse, and report

Features
--------
1.  parse_log_file(path)            - parse structured log entries
2.  filter_by_level(entries, level) - keep one severity level
3.  filter_by_module(entries, mod)  - keep entries from one module
4.  count_by_level(entries)         - frequency table per level
5.  count_by_module(entries)        - frequency table per module
6.  find_errors(entries)            - all ERROR + CRITICAL entries
7.  detect_repeated_messages(entries, n) - messages appearing >= n times
8.  extract_ips(entries)            - all IP addresses found
9.  timeline(entries, interval)     - entries bucketed by minute/hour
10. generate_report(entries)        - full text summary report
11. export_to_csv(entries, path)    - save filtered entries as CSV

Run:
    python log_processor.py
    python log_processor.py --log server_events.log --level ERROR
"""

import re
import csv
import argparse
import os
from collections import Counter


# ─────────────────────────────────────────────────────────────────────────────
# DATA MODEL  — each entry is a plain dict
# ─────────────────────────────────────────────────────────────────────────────
# {
#   "timestamp": "2024-01-15 09:00:01",
#   "level":     "INFO",
#   "module":    "auth",
#   "message":   "User 'alice' logged in from 192.168.1.10"
# }

LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

# Regex: DATE TIME LEVEL [MODULE] MESSAGE
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+"
    r"\[(?P<module>[^\]]+)\]\s+"
    r"(?P<message>.+)$"
)

IP_PATTERN = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


# ─────────────────────────────────────────────────────────────────────────────
# PARSING
# ─────────────────────────────────────────────────────────────────────────────

def parse_line(line: str) -> dict | None:
    """Parse one log line. Returns a dict or None if the line is invalid."""
    line = line.strip()
    if not line:
        return None
    m = LOG_PATTERN.match(line)
    if not m:
        return None
    return {
        "timestamp": m.group("timestamp"),
        "level":     m.group("level").strip(),
        "module":    m.group("module").strip(),
        "message":   m.group("message").strip(),
    }


def parse_log_file(path: str) -> list:
    """Read a log file and return a list of valid entry dicts."""
    if not os.path.exists(path):
        print(f"ERROR: File not found: {path!r}")
        return []
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            entry = parse_line(line)
            if entry:
                entries.append(entry)
    print(f"  Parsed {len(entries)} entries from {path!r}")
    return entries


# ─────────────────────────────────────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────────────────────────────────────

def filter_by_level(entries: list, level: str) -> list:
    """Return entries whose level exactly matches *level* (case-insensitive)."""
    level = level.upper()
    return [e for e in entries if e["level"] == level]


def filter_by_module(entries: list, module: str) -> list:
    """Return entries whose module matches *module* (case-insensitive)."""
    module = module.lower()
    return [e for e in entries if e["module"].lower() == module]


def find_errors(entries: list) -> list:
    """Return all ERROR and CRITICAL entries."""
    return [e for e in entries if e["level"] in ("ERROR", "CRITICAL")]


# ─────────────────────────────────────────────────────────────────────────────
# ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────

def count_by_level(entries: list) -> dict:
    """Return {level: count} for every log level."""
    counts = Counter(e["level"] for e in entries)
    # Return in canonical order
    return {lvl: counts.get(lvl, 0) for lvl in LOG_LEVELS}


def count_by_module(entries: list) -> dict:
    """Return {module: count} sorted by count descending."""
    counts = Counter(e["module"] for e in entries)
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def detect_repeated_messages(entries: list, min_count: int = 2) -> list:
    """Find messages that appear >= *min_count* times.

    Returns list of {"message": ..., "count": ..., "level": ...}.
    """
    counter = Counter(e["message"] for e in entries)
    results = []
    for msg, cnt in counter.items():
        if cnt >= min_count:
            # Find the level of the first occurrence
            lvl = next((e["level"] for e in entries if e["message"] == msg), "?")
            results.append({"message": msg, "count": cnt, "level": lvl})
    return sorted(results, key=lambda x: x["count"], reverse=True)


def extract_ips(entries: list) -> list:
    """Return a sorted list of unique IP addresses found in any message."""
    ips = set()
    for e in entries:
        ips.update(IP_PATTERN.findall(e["message"]))
    return sorted(ips)


def timeline(entries: list, interval: str = "minute") -> dict:
    """Bucket entries by time interval.

    interval: "minute" -> "YYYY-MM-DD HH:MM"
              "hour"   -> "YYYY-MM-DD HH"
    """
    buckets: dict = {}
    for e in entries:
        ts = e["timestamp"]
        if interval == "hour":
            key = ts[:13]          # "2024-01-15 09"
        else:
            key = ts[:16]          # "2024-01-15 09:00"
        buckets.setdefault(key, []).append(e)
    return dict(sorted(buckets.items()))


# ─────────────────────────────────────────────────────────────────────────────
# REPORTING
# ─────────────────────────────────────────────────────────────────────────────

def generate_report(entries: list) -> str:
    """Build a formatted multi-section text report and return it as a string."""
    lines = []
    w = 60

    lines.append("=" * w)
    lines.append("  LOG ANALYSIS REPORT")
    lines.append("=" * w)
    lines.append(f"  Total entries  : {len(entries)}")
    if entries:
        lines.append(f"  First entry    : {entries[0]['timestamp']}")
        lines.append(f"  Last entry     : {entries[-1]['timestamp']}")

    # Level breakdown
    lines.append("")
    lines.append("  LEVEL BREAKDOWN")
    lines.append("  " + "-" * (w - 2))
    level_counts = count_by_level(entries)
    total = len(entries) or 1
    for lvl, cnt in level_counts.items():
        bar = "#" * cnt
        pct = cnt / total * 100
        lines.append(f"  {lvl:<10} {cnt:>4}  {pct:>5.1f}%  {bar}")

    # Module breakdown
    lines.append("")
    lines.append("  MODULE BREAKDOWN")
    lines.append("  " + "-" * (w - 2))
    for mod, cnt in count_by_module(entries).items():
        lines.append(f"  [{mod}]  {cnt} entries")

    # Errors & criticals
    errors = find_errors(entries)
    lines.append("")
    lines.append(f"  ERRORS & CRITICALS  ({len(errors)} found)")
    lines.append("  " + "-" * (w - 2))
    for e in errors:
        lines.append(f"  [{e['level']}] {e['timestamp']}  {e['message'][:50]}")

    # Repeated messages
    repeated = detect_repeated_messages(entries, min_count=2)
    if repeated:
        lines.append("")
        lines.append("  REPEATED MESSAGES")
        lines.append("  " + "-" * (w - 2))
        for item in repeated:
            lines.append(f"  x{item['count']}  [{item['level']}]  {item['message'][:50]}")

    # IPs
    ips = extract_ips(entries)
    if ips:
        lines.append("")
        lines.append("  IP ADDRESSES FOUND")
        lines.append("  " + "-" * (w - 2))
        for ip in ips:
            lines.append(f"  {ip}")

    lines.append("")
    lines.append("=" * w)
    return "\n".join(lines)


def export_to_csv(entries: list, path: str) -> None:
    """Write entries to a CSV file."""
    fieldnames = ["timestamp", "level", "module", "message"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)
    print(f"  Exported {len(entries)} rows -> {path}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_log = os.path.join(script_dir, "server_events.log")
    default_out = os.path.join(script_dir, "reports")

    parser = argparse.ArgumentParser(description="Advanced log processor")
    parser.add_argument("--log",    default=default_log)
    parser.add_argument("--level",  default="",
                        help="Filter to one level (INFO/WARNING/ERROR/CRITICAL)")
    parser.add_argument("--module", default="",
                        help="Filter to one module (api/db/auth/security)")
    parser.add_argument("--out-dir", default=default_out, help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    print("=" * 60)
    print("  LOG PROCESSOR")
    print("=" * 60)

    # 1. Parse
    entries = parse_log_file(args.log)
    if not entries:
        return

    # 2. Optional filter
    if args.level:
        entries = filter_by_level(entries, args.level)
        print(f"  Filtered to level={args.level!r}: {len(entries)} entries")
    if args.module:
        entries = filter_by_module(entries, args.module)
        print(f"  Filtered to module={args.module!r}: {len(entries)} entries")

    # 3. Generate and print report
    report = generate_report(entries)
    print()
    print(report)

    # 4. Export CSV
    csv_path = os.path.join(args.out_dir, "processed_log.csv")
    export_to_csv(entries, csv_path)

    # 5. Save report as text
    report_path = os.path.join(args.out_dir, "log_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"  Report saved  -> {report_path}")

    print()
    print("Log processing complete!")


if __name__ == "__main__":
    main()
