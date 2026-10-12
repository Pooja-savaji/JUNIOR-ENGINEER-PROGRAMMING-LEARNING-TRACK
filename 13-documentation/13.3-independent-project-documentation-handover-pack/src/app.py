
import json
from pathlib import Path

DATA = Path("data/tasks.json")
def load_tasks():
    DATA.parent.mkdir(parents=True, exist_ok=True)

    if not DATA.exists():
        DATA.write_text("[]", encoding="utf-8")

    return json.loads(DATA.read_text(encoding="utf-8"))
def add_task(title):
    if not title.strip():
        raise ValueError("Task title cannot be empty")

    tasks = load_tasks()
    tasks.append({
        "id": len(tasks) + 1,
        "title": title,
        "completed": False
    })
    DATA.write_text(json.dumps(tasks, indent=4), encoding="utf-8")
    print("Task added successfully!")

def main():
    title = input("Enter task: ")
    add_task(title)

if __name__ == "__main__":
    main()
