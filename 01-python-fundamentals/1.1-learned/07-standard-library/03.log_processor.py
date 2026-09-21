from pathlib import Path
from collections import Counter
import re

log_file = Path("app.log")
text = log_file.read_text()
levels = re.findall(r"\b(INFO|WARNING|ERROR)\b", text)
count = Counter(levels)
print("Log Summary")

for level, total in count.items():
    print(level, ":", total)
