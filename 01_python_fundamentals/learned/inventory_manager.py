"""Simple Inventory Management System (Beginner Friendly).

Demonstrates:
- Managing collections of dictionary records
- Adding, updating, and removing inventory items
- Stock tracking, restock / sale operations, and low-stock alerts
- Total inventory valuation calculation
"""


class InventoryManager:
    """Manages store/warehouse products and stock levels."""

    def __init__(self):
        # Sample starter inventory
        self.inventory = [
            {"id": "P101", "name": "Wireless Mouse", "category": "Accessories", "price": 25.00, "stock": 15},
            {"id": "P102", "name": "Mechanical Keyboard", "category": "Accessories", "price": 80.00, "stock": 4},
            {"id": "P103", "name": "27-inch Monitor", "category": "Displays", "price": 250.00, "stock": 8},
            {"id": "P104", "name": "USB-C Cable", "category": "Cables", "price": 10.00, "stock": 2},
            {"id": "P105", "name": "Ergonomic Chair", "category": "Furniture", "price": 180.00, "stock": 6},
        ]

    def add_product(self, product_id: str, name: str, category: str, price: float, stock: int):
        """Add a new product to the inventory."""
        # Check if product ID already exists
        for item in self.inventory:
            if item["id"].lower() == product_id.strip().lower():
                print(f"[Error] Product ID '{product_id}' already exists!")
                return False

        new_item = {
            "id": product_id.strip().upper(),
            "name": name.strip(),
            "category": category.strip(),
            "price": round(float(price), 2),
            "stock": int(stock),
        }
        self.inventory.append(new_item)
        print(f"[Success] Added product: {new_item['name']} ({new_item['id']})")
        return True

    def update_stock(self, product_id: str, quantity_change: int) -> bool:
        """Add or subtract stock (positive to restock, negative for sale)."""
        for item in self.inventory:
            if item["id"].lower() == product_id.strip().lower():
                new_stock = item["stock"] + quantity_change
                if new_stock < 0:
                    print(f"[Error] Not enough stock! Current stock is {item['stock']}.")
                    return False
                item["stock"] = new_stock
                action = "Restocked" if quantity_change > 0 else "Sold"
                print(f"[Success] {action} {abs(quantity_change)} units of '{item['name']}'. New stock: {item['stock']}")
                return True
        print(f"[Error] Product ID '{product_id}' not found.")
        return False

    def list_products(self, items=None):
        """Print inventory items in a clean table format."""
        display_list = items if items is not None else self.inventory
        print("\n" + "=" * 65)
        print(f"{'ID':<6} | {'Product Name':<22} | {'Category':<14} | {'Price':>8} | {'Stock':>5}")
        print("=" * 65)
        if not display_list:
            print("  [No products found]")
        else:
            for item in display_list:
                stock_alert = f"{item['stock']} ⚠️" if item['stock'] < 5 else f"{item['stock']}"
                print(f"{item['id']:<6} | {item['name']:<22} | {item['category']:<14} | ${item['price']:>7.2f} | {stock_alert:>5}")
        print("=" * 65)

    def get_low_stock_items(self, threshold: int = 5) -> list:
        """Find items where stock is below the threshold."""
        return [item for item in self.inventory if item["stock"] < threshold]

    def calculate_total_valuation(self) -> float:
        """Calculate the total retail value of all products in stock."""
        total = sum(item["price"] * item["stock"] for item in self.inventory)
        return round(total, 2)


def run_inventory_demo():
    print("=" * 55)
    print("        📦 INVENTORY MANAGEMENT DEMO           ")
    print("=" * 55)

    inv = InventoryManager()

    # 1. View initial inventory
    print("\n1. Initial Inventory List:")
    inv.list_products()

    # 2. Total Valuation
    total_val = inv.calculate_total_valuation()
    print(f"\nTotal Inventory Value: ${total_val:,.2f}")

    # 3. Restock & Sales
    print("\n2. Updating Stock Levels:")
    inv.update_stock("P104", 20)   # Restock USB-C Cables (+20)
    inv.update_stock("P101", -5)   # Sold 5 Wireless Mice (-5)

    # 4. Low stock check
    print("\n3. Low Stock Items (Stock < 5):")
    low_stock = inv.get_low_stock_items(threshold=5)
    inv.list_products(low_stock)

    # 5. Add new product
    print("\n4. Adding New Product:")
    inv.add_product("P106", "Laptop Stand", "Accessories", 35.50, 12)
    inv.list_products()


if __name__ == "__main__":
    run_inventory_demo()
