import csv
from log_parser import parse_log_file


records, summary = parse_log_file("app.log")

with open("log_report.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow(["Log Level", "Count"])

    for level, count in summary.items():
        writer.writerow([level, count])

    writer.writerow([])

    writer.writerow([
        "Date",
        "Time",
        "Level",
        "Message"
    ])

    for record in records:
        writer.writerow([
            record["date"],
            record["time"],
            record["level"],
            record["message"]
        ])

print("CSV report created successfully.")
