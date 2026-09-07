"""Demonstration script showcasing formatting and validator utilities."""

from app.utils.formatting import format_asset_id, format_currency, format_date
from app.utils.validators import is_non_empty_string, is_valid_asset_tag, is_valid_email


def run_demo():
    print("=== ASSET TRACKER UTILITIES DEMO ===\n")
    
    # 1. Formatting Tests
    print("--- 1. Formatting Utilities ---")
    print(f"format_currency(1249.99)       -> {format_currency(1249.99)}")
    print(f"format_currency(-45.5)         -> {format_currency(-45.5)}")
    print(f"format_date('2026-09-07')      -> {format_date('2026-09-07')}")
    print(f"format_asset_id(42)            -> {format_asset_id(42)}")
    print(f"format_asset_id(105, 'SRV', 5) -> {format_asset_id(105, 'SRV', 5)}")
    
    # 2. Validation Tests
    print("\n--- 2. Validation Utilities ---")
    tags = ["AST-000123", "SRV-00456", "bad_tag", ""]
    for t in tags:
        print(f"is_valid_asset_tag('{t}') -> {is_valid_asset_tag(t)}")
        
    emails = ["pooja@company.com", "admin.it@delta-iot.org", "invalid-email@", ""]
    for e in emails:
        print(f"is_valid_email('{e}') -> {is_valid_email(e)}")
        
    strings = ["Dell XPS 15", "   ", None, "Server Room B"]
    for s in strings:
        print(f"is_non_empty_string({repr(s)}) -> {is_non_empty_string(s)}")

    print("\nAll utility functions tested successfully!")


if __name__ == "__main__":
    run_demo()
