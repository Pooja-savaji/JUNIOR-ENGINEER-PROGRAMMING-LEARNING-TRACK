"""Menu Loops and User Input Patterns in Python (Beginner Friendly).

Demonstrates:
- Pattern 1: Classic while True Loop with if/elif/else
- Pattern 2: Safe Input Validation Loop (prevents program crashes)
- Pattern 3: Confirmation Prompts (yes/no)
- Pattern 4: A Complete Interactive Contact Book
"""


# --- 1. INPUT VALIDATION HELPERS ---

def get_valid_integer(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Safely prompt the user for an integer within an optional range."""
    while True:
        user_input = input(prompt).strip()
        try:
            val = int(user_input)
            if min_val is not None and val < min_val:
                print(f"[Error] Please enter a number >= {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"[Error] Please enter a number <= {max_val}.")
                continue
            return val
        except ValueError:
            print("[Error] Invalid input. Please enter a whole number.")


def get_non_empty_string(prompt: str) -> str:
    """Prompt the user until they provide a non-blank string."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("[Error] Input cannot be empty. Please enter some text.")


def ask_yes_no(prompt: str) -> bool:
    """Ask user a Yes/No question and return True for Yes, False for No."""
    while True:
        ans = input(f"{prompt} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        elif ans in ("n", "no"):
            return False
        print("[Error] Please type 'y' for Yes or 'n' for No.")


# --- 2. COMPLETE MENU APPLICATION EXAMPLE ---

class MiniContactBook:
    """Simple in-memory contact manager demonstrating menu loop operations."""

    def __init__(self):
        self.contacts = [
            {"name": "Alice Smith", "phone": "555-0101", "email": "alice@example.com"},
            {"name": "Bob Jones", "phone": "555-0102", "email": "bob@example.com"},
        ]

    def list_contacts(self):
        print("\n" + "-" * 50)
        print(f"{'#':<3} | {'Name':<18} | {'Phone':<12} | {'Email'}")
        print("-" * 50)
        if not self.contacts:
            print("  [No contacts found]")
        else:
            for idx, c in enumerate(self.contacts, 1):
                print(f"{idx:<3} | {c['name']:<18} | {c['phone']:<12} | {c['email']}")
        print("-" * 50)

    def add_contact(self):
        print("\n--- Add New Contact ---")
        name = get_non_empty_string("Contact Name: ")
        phone = get_non_empty_string("Phone Number: ")
        email = get_non_empty_string("Email Address: ")
        self.contacts.append({"name": name, "phone": phone, "email": email})
        print(f"[Success] Added '{name}' to contact book.")

    def search_contact(self):
        print("\n--- Search Contact ---")
        term = get_non_empty_string("Enter name to search: ").lower()
        results = [c for c in self.contacts if term in c["name"].lower()]
        print(f"\nFound {len(results)} match(es):")
        for c in results:
            print(f"  • {c['name']} | Phone: {c['phone']} | Email: {c['email']}")

    def delete_contact(self):
        self.list_contacts()
        if not self.contacts:
            return
        print("\n--- Delete Contact ---")
        choice = get_valid_integer(f"Enter contact # to delete (1-{len(self.contacts)}): ", 1, len(self.contacts))
        removed = self.contacts.pop(choice - 1)
        print(f"[Success] Removed '{removed['name']}'.")


def run_menu_loop_demo():
    """Main interactive menu loop."""
    app = MiniContactBook()

    print("=" * 50)
    print("         📋 MENU LOOPS & INPUT DEMO            ")
    print("=" * 50)

    while True:
        print("\nMain Menu:")
        print("  1. 👥 List Contacts")
        print("  2. ➕ Add Contact")
        print("  3. 🔍 Search Contact")
        print("  4. ❌ Delete Contact")
        print("  0. 🚪 Exit")

        choice = input("\nEnter choice (0-4): ").strip()

        if choice == "1":
            app.list_contacts()
        elif choice == "2":
            app.add_contact()
        elif choice == "3":
            app.search_contact()
        elif choice == "4":
            app.delete_contact()
        elif choice == "0":
            if ask_yes_no("Are you sure you want to exit?"):
                print("\nGoodbye! Thanks for using Menu Loops Demo. 👋\n")
                break
        else:
            print("[Error] Invalid option. Please enter a number from 0 to 4.")


if __name__ == "__main__":
    run_menu_loop_demo()
