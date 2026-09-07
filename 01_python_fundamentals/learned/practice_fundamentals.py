"""Day 1: Python Fundamentals Practice Script."""

def demonstrate_fundamentals():
    # 1. Variables and Type Conversion
    asset_name: str = "Dell Latitude 5420"
    unit_cost: float = 1249.99
    quantity: int = 5
    is_active: bool = True
    
    total_cost: float = unit_cost * quantity
    print(f"[Item] {asset_name} | Qty: {quantity} | Unit: ${unit_cost:.2f} | Total: ${total_cost:,.2f}")
    
    # 2. Conditionals & Expressions
    if total_cost > 5000:
        approval_tier = "Tier 2 (Manager Approval Required)"
    else:
        approval_tier = "Tier 1 (Auto-approved)"
    print(f"[Status] {approval_tier}")

    # 3. Collection iteration with fundamentals
    categories = ["Laptop", "Monitor", "Docking Station", "Keyboard"]
    print("\nAsset Categories:")
    for idx, cat in enumerate(categories, start=1):
        print(f"  {idx}. {cat}")

if __name__ == "__main__":
    demonstrate_fundamentals()
