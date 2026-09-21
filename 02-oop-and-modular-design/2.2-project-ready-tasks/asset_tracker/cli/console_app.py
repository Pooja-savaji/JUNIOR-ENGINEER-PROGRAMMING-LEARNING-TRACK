"""
console_app.py
Production-grade terminal presentation layer for Asset Tracker.
"""

from __future__ import annotations
import sys
from datetime import date
from typing import Optional

from ..services.asset_service import AssetService
from ..models.asset import AssetCategory, AssetStatus, HardwareAsset, SoftwareLicense
from ..exceptions.errors import AssetTrackerError


class ConsoleApp:
    """Interactive command-line interface for Asset Management System."""

    def __init__(self, service: AssetService) -> None:
        self.service = service

    def run_menu(self) -> None:
        """Main interactive loop."""
        while True:
            self._print_banner()
            print("  1. List All Assets")
            print("  2. Check Out Asset to Employee")
            print("  3. Check In Asset from Employee")
            print("  4. View Employee Custody & Deployments")
            print("  5. View Asset Audit History")
            print("  6. Maintenance Management")
            print("  7. Financial Depreciation & Valuation Report")
            print("  8. Operational Audit Summary")
            print("  9. Run Automated End-to-End Demo")
            print("  0. Exit")
            print("-" * 65)

            choice = input("Select an option [0-9]: ").strip()
            if choice == "1":
                self._handle_list_assets()
            elif choice == "2":
                self._handle_checkout()
            elif choice == "3":
                self._handle_checkin()
            elif choice == "4":
                self._handle_employee_assets()
            elif choice == "5":
                self._handle_asset_history()
            elif choice == "6":
                self._handle_maintenance()
            elif choice == "7":
                self._handle_valuation()
            elif choice == "8":
                self._handle_audit_summary()
            elif choice == "9":
                self.run_demo()
            elif choice == "0":
                print()
                print("Exiting IT Asset Tracker. Goodbye!")
                break
            else:
                print()
                print("[!] Invalid selection. Please try again.")

    def _print_banner(self) -> None:
        print()
        print("=" * 65)
        print("  DELTA IOT — ENTERPRISE IT ASSET MANAGEMENT SYSTEM")
        print("=" * 65)

    def _handle_list_assets(self) -> None:
        print()
        print("--- INVENTORY LISTING ---")
        assets = self.service.list_assets()
        if not assets:
            print("  No assets registered in inventory.")
            return

        w = 90
        print("-" * w)
        print(f"  {'ID':<10} {'NAME':<24} {'CATEGORY':<16} {'STATUS':<18} {'CURRENT VAL':>12}")
        print("-" * w)
        for a in assets:
            val = a.calculate_current_value()
            print(f"  {a.asset_id:<10} {a.name[:22]:<24} {a.category.value:<16} {a.status.value:<18} ${val:>11,.2f}")
        print("-" * w)

    def _handle_checkout(self) -> None:
        print()
        print("--- CHECK OUT ASSET ---")
        aid = input("Enter Asset ID (e.g. AST-1001): ").strip()
        eid = input("Enter Employee ID (e.g. EMP-101): ").strip()
        cond = input("Condition (default: Good): ").strip() or "Good"
        note = input("Assignment notes: ").strip()

        try:
            asn = self.service.checkout_asset(aid, eid, condition=cond, notes=note)
            print()
            print(f"[+] SUCCESS: Asset {aid} checked out to {eid}. Assignment ID: {asn.assignment_id}")
        except AssetTrackerError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_checkin(self) -> None:
        print()
        print("--- CHECK IN ASSET ---")
        aid = input("Enter Asset ID to check in: ").strip()
        cond = input("Condition on return: ").strip() or "Good"
        note = input("Return notes: ").strip()

        try:
            asn = self.service.checkin_asset(aid, condition=cond, return_notes=note)
            print()
            print(f"[+] SUCCESS: Asset {aid} successfully returned to inventory.")
        except AssetTrackerError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_employee_assets(self) -> None:
        print()
        print("--- EMPLOYEE CUSTODY LOOKUP ---")
        eid = input("Enter Employee ID: ").strip()
        try:
            emp = self.service.get_employee(eid)
            assets = self.service.get_employee_assets(eid)
            print()
            print(f"Employee: {emp.name} ({emp.emp_id}) | Dept: {emp.department} | Email: {emp.email}")
            print(f"Assigned Items ({len(assets)}):")
            if not assets:
                print("  No assets currently assigned to this employee.")
            for a in assets:
                print(f"  * [{a.category.value}] {a.asset_id} - {a.name} (Value: ${a.calculate_current_value():,.2f})")
        except AssetTrackerError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_asset_history(self) -> None:
        print()
        print("--- ASSET AUDIT HISTORY ---")
        aid = input("Enter Asset ID: ").strip()
        try:
            asset = self.service.get_asset(aid)
            history = self.service.get_asset_history(aid)
            print()
            print(f"Audit History for {asset.name} ({asset.asset_id}):")
            if not history:
                print("  No past assignment events recorded.")
            for rec in history:
                ret_str = rec.returned_at.strftime('%Y-%m-%d %H:%M') if rec.returned_at else 'ACTIVE DEPLOYMENT'
                print(f"  * {rec.assignment_id}: Assigned to {rec.emp_id} at {rec.assigned_at.strftime('%Y-%m-%d')} -> {ret_str}")
        except AssetTrackerError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_maintenance(self) -> None:
        print()
        print("--- MAINTENANCE MENU ---")
        print("  1. Send Asset to Maintenance")
        print("  2. Return Asset from Maintenance")
        sub = input("Selection [1-2]: ").strip()
        aid = input("Enter Asset ID: ").strip()

        try:
            if sub == "1":
                self.service.send_to_maintenance(aid)
                print()
                print(f"[+] Asset {aid} marked as UNDER_MAINTENANCE.")
            elif sub == "2":
                self.service.return_from_maintenance(aid)
                print()
                print(f"[+] Asset {aid} restored to IN_STOCK.")
            else:
                print()
                print("[-] Invalid selection.")
        except AssetTrackerError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_valuation(self) -> None:
        report = self.service.calculate_inventory_valuation()
        print()
        print("=" * 65)
        print(f"  FINANCIAL INVENTORY VALUATION (As of {report['as_of_date']})")
        print("=" * 65)
        print(f"  Total Assets Tracked      : {report['asset_count']:>10}")
        print(f"  Total Acquisition Cost    : ${report['total_acquisition_cost']:>12,.2f}")
        print(f"  Total Current Book Value  : ${report['total_depreciated_value']:>12,.2f}")
        print(f"  Accumulated Depreciation  : ${report['accumulated_depreciation']:>12,.2f}")
        print("-" * 65)
        print("  Category Breakdown:")
        for cat, data in report["by_category"].items():
            print(f"    * {cat:<18}: {data['count']:>2} units | Cost: ${data['acquisition']:>9,.2f} | Value: ${data['current_value']:>9,.2f}")
        print("=" * 65)

    def _handle_audit_summary(self) -> None:
        audit = self.service.generate_audit_report()
        print()
        print("=" * 65)
        print("  OPERATIONAL AUDIT SUMMARY")
        print("=" * 65)
        print(f"  Total Inventory Size      : {audit['total_assets']:>5}")
        print(f"  In Stock (Available)      : {audit['in_stock']:>5}")
        print(f"  Deployed / Assigned       : {audit['assigned']:>5}")
        print(f"  Under Maintenance         : {audit['under_maintenance']:>5}")
        print(f"  Decommissioned (Retired)  : {audit['retired']:>5}")
        print(f"  Hardware Utilization Rate : {audit['utilization_rate_pct']:>5.1f}%")
        print(f"  Total Registered Personnel: {audit['total_employees']:>5}")
        print("=" * 65)

    def run_demo(self) -> None:
        """Automated walkthrough of all domain operations."""
        print()
        print("=" * 65)
        print("  EXECUTING AUTOMATED ENTERPRISE DEMO WALKTHROUGH")
        print("=" * 65)

        # 1. Inventory Valuation
        self._handle_valuation()

        # 2. Operational Audit
        self._handle_audit_summary()

        # 3. Simulate Checkout
        print()
        print("[Demo Step 1] Deploying ThinkPad to Alice Smith (EMP-101)...")
        try:
            asn1 = self.service.checkout_asset("AST-1001", "EMP-101", condition="Mint", notes="New developer kit")
            print(f"  Checkout confirmed: {asn1}")
        except Exception as e:
            print(f"  Notice: {e}")

        # 4. Invariant Protection: Double Checkout
        print()
        print("[Demo Step 2] Invariant Protection: Attempting Double Checkout of AST-1001...")
        try:
            self.service.checkout_asset("AST-1001", "EMP-102")
        except AssetTrackerError as err:
            print(f"  [Expected Domain Exception Caught]: {err}")

        # 5. Software License Allocation
        print()
        print("[Demo Step 3] Allocating JetBrains Ultimate seat to Bob Jones (EMP-102)...")
        try:
            asn2 = self.service.checkout_asset("AST-1004", "EMP-102", notes="Backend engineering")
            print(f"  License seat assigned: {asn2}")
            lic = self.service.get_asset("AST-1004")
            print(f"  Remaining seats on AST-1004: {lic.available_seats}/{lic.total_seats}")
        except Exception as e:
            print(f"  Notice: {e}")

        # 6. Check In & Condition Log
        print()
        print("[Demo Step 4] Returning AST-1001 back to Warehouse Stock...")
        try:
            returned = self.service.checkin_asset("AST-1001", condition="Good", return_notes="Project concluded")
            print(f"  Checkin confirmed: {returned}")
        except Exception as e:
            print(f"  Notice: {e}")

        # 7. Audit History
        print()
        print("[Demo Step 5] Auditing Life-Cycle Event Stream for AST-1001:")
        history = self.service.get_asset_history("AST-1001")
        for rec in history:
            print(f"  - {rec}")

        print()
        print("Demo Walkthrough Complete!")
