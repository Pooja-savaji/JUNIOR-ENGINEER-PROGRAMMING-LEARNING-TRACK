from pathlib import Path

LOG_LEVELS = {"INFO", "WARNING", "ERROR"}


def parse_log_file(file_path):
    records = []
    summary = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    try:
        lines = Path(file_path).read_text().splitlines()
    except FileNotFoundError:
        print("Log file not found.")
        return records, summary

    for line in lines:
        parts = line.split(" ", 3)

        if len(parts) != 4:
            print("Skipping invalid line:", line)
            continue

        date, time, level, message = parts

        if level not in LOG_LEVELS:
            print("Skipping unsupported level:", level)
            continue

        records.append({
            "date": date,
            "time": time,
            "level": level,
            "message": message
        })

        summary[level] += 1

    return records, summary


if __name__ == "__main__":
    records, summary = parse_log_file("app.log")

    print("\nLog Summary")
    print("-----------")

    for level, count in summary.items():
        print(f"{level}: {count}")
