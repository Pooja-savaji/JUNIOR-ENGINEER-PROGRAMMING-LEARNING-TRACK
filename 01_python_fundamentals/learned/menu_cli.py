"""Reusable Menu-Driven CLI Framework & Mini Task Manager.

Demonstrates: modular menu loops, clear screen transitions, formatted tabular
presentation, state manipulation, validation, and defensive programming.
"""

import sys
from datetime import datetime
from typing import Callable, Dict, List, Optional


class TaskItem:
    """Represents a single task record in the CLI system."""

    def __init__(self, task_id: int, title: str, priority: str = "Medium") -> None:
        self.id = task_id
        self.title = title.strip()
        self.priority = priority.capitalize()
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def toggle(self) -> None:
        self.completed = not self.completed

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at,
        }


class MenuCLIApp:
    """Extensible Menu-driven CLI Application."""

    def __init__(self, app_title: str = "Mini Task & Item Manager") -> None:
        self.app_title = app_title
        self.tasks: List[TaskItem] = []
        self._next_id = 1

    def add_task(self, title: str, priority: str = "Medium") -> TaskItem:
        task = TaskItem(self._next_id, title, priority)
        self.tasks.append(task)
        self._next_id += 1
        return task

    def delete_task(self, task_id: int) -> bool:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        return len(self.tasks) < before

    def find_task(self, task_id: int) -> Optional[TaskItem]:
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def display_tasks(self, filter_completed: Optional[bool] = None) -> None:
        filtered = self.tasks
        if filter_completed is not None:
            filtered = [t for t in self.tasks if t.completed == filter_completed]

        print("\n" + "=" * 70)
        print(f"{'ID':<5} | {'Status':<10} | {'Priority':<10} | {'Created':<16} | {'Title'}")
        print("=" * 70)

        if not filtered:
            print("  [No items to display]")
        else:
            for t in filtered:
                status = "✅ Done" if t.completed else "⏳ Pending"
                print(f"{t.id:<5} | {status:<10} | {t.priority:<10} | {t.created_at:<16} | {t.title}")
        print("=" * 70)


def prompt_add(app: MenuCLIApp) -> None:
    print("\n--- ➕ Add New Task ---")
    while True:
        title = input("Enter task title: ").strip()
        if title:
            break
        print("[Error] Title cannot be blank.")

    print("Select Priority: 1. Low  2. Medium  3. High (default: 2)")
    p_choice = input("Choice (1-3): ").strip()
    priority_map = {"1": "Low", "2": "Medium", "3": "High"}
    priority = priority_map.get(p_choice, "Medium")

    item = app.add_task(title, priority)
    print(f"\n[Success] Created task #{item.id}: '{item.title}' [{item.priority}]")


def prompt_toggle(app: MenuCLIApp) -> None:
    app.display_tasks()
    print("\n--- 🔄 Toggle Task Status ---")
    raw = input("Enter Task ID to toggle: ").strip()
    try:
        t_id = int(raw)
        task = app.find_task(t_id)
        if task:
            task.toggle()
            status = "Completed ✅" if task.completed else "Pending ⏳"
            print(f"\n[Success] Task #{task.id} marked as {status}.")
        else:
            print(f"[Error] Task #{t_id} not found.")
    except ValueError:
        print("[Error] Please enter a valid numeric ID.")


def prompt_delete(app: MenuCLIApp) -> None:
    app.display_tasks()
    print("\n--- ❌ Delete Task ---")
    raw = input("Enter Task ID to delete: ").strip()
    try:
        t_id = int(raw)
        if app.delete_task(t_id):
            print(f"\n[Success] Task #{t_id} deleted successfully.")
        else:
            print(f"[Error] Task #{t_id} not found.")
    except ValueError:
        print("[Error] Please enter a valid numeric ID.")


def prompt_search(app: MenuCLIApp) -> None:
    print("\n--- 🔍 Search Tasks ---")
    query = input("Enter keyword to search: ").strip().lower()
    if not query:
        print("[Error] Search query cannot be empty.")
        return

    matches = [t for t in app.tasks if query in t.title.lower() or query in t.priority.lower()]
    print(f"\nFound {len(matches)} matching tasks:")
    print("=" * 70)
    for t in matches:
        status = "✅ Done" if t.completed else "⏳ Pending"
        print(f"{t.id:<5} | {status:<10} | {t.priority:<10} | {t.title}")
    print("=" * 70)


def run_menu_cli():
    """Main interactive loop."""
    app = MenuCLIApp()

    # Pre-populate sample tasks
    app.add_task("Review Python Fundamentals §4", "High")
    app.add_task("Set up Git repository scaffolding", "Medium")
    app.add_task("Write unit tests for validators", "Low")

    while True:
        print("\n" + "#" * 50)
        print(f"       🖥️  {app.app_title.upper()}       ")
        print("#" * 50)
        print("  1. 📋 View All Tasks")
        print("  2. ➕ Add Task")
        print("  3. 🔄 Toggle Completed / Pending")
        print("  4. 🔍 Search Tasks")
        print("  5. ❌ Delete Task")
        print("  6. 📊 Task Summary Statistics")
        print("  0. 🚪 Exit Application")
        print("#" * 50)

        choice = input("\nEnter choice (0-6): ").strip()

        if choice == "0":
            print("\nExiting Application. Have a productive day! 👋\n")
            break
        elif choice == "1":
            app.display_tasks()
        elif choice == "2":
            prompt_add(app)
        elif choice == "3":
            prompt_toggle(app)
        elif choice == "4":
            prompt_search(app)
        elif choice == "5":
            prompt_delete(app)
        elif choice == "6":
            total = len(app.tasks)
            done = sum(1 for t in app.tasks if t.completed)
            pending = total - done
            pct = (done / total * 100) if total > 0 else 0.0
            print("\n" + "-" * 35)
            print("        TASK SUMMARY        ")
            print("-" * 35)
            print(f"Total Tasks    : {total}")
            print(f"Completed      : {done} ({pct:.1f}%)")
            print(f"Pending        : {pending}")
            print("-" * 35)
        else:
            print("[Error] Invalid choice. Please choose a number from 0 to 6.")


if __name__ == "__main__":
    run_menu_cli()
