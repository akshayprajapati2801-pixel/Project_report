
# ==========================================
# Hospital Management System
# Dashboard with MySQL Counts
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox

from core.session import Session
from database.connection import Database

from ui.customers.customer_list import CustomerList
from ui.products.product_list import ProductList
from ui.suppliers.supplier_list import SupplierList
from ui.employees.employee_list import EmployeeList
from ui.sales.sales_list import SalesList
from ui.purchases.purchase_list import PurchaseList


class Dashboard:

    def __init__(self, root, logout_callback):
        self.root = root
        self.logout_callback = logout_callback
        self.database = Database()
        self.create_dashboard()

    # --------------------------------------
    # Create Dashboard
    # --------------------------------------

    def create_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Hospital Management System")
        self.root.geometry("1200x700")
        self.root.minsize(950, 600)
        self.root.resizable(True, True)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        self.sidebar = ttk.Frame(
            main_frame,
            width=220,
            padding=15
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content = ttk.Frame(
            main_frame,
            padding=30
        )
        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()
        self.show_dashboard()

    # --------------------------------------
    # Sidebar
    # --------------------------------------

    def create_sidebar(self):
        ttk.Label(
            self.sidebar,
            text="HOSPITAL",
            font=("Arial", 18, "bold")
        ).pack(pady=(10, 5))

        ttk.Label(
            self.sidebar,
            text="Management System",
            font=("Arial", 9)
        ).pack(pady=(0, 30))

        self.create_menu_button("Dashboard", self.show_dashboard)
        self.create_menu_button("Patients", self.show_patients)
        self.create_menu_button("Medicines", self.show_medicines)
        self.create_menu_button("Suppliers", self.show_suppliers)
        self.create_menu_button("Sales / Billing", self.show_sales)
        self.create_menu_button("Purchases", self.show_purchases)
        self.create_menu_button("Employees", self.show_employees)

        ttk.Button(
            self.sidebar,
            text="Logout",
            command=self.logout_callback
        ).pack(side="bottom", fill="x", pady=10)

    def create_menu_button(self, text, command):
        ttk.Button(
            self.sidebar,
            text=text,
            command=command
        ).pack(fill="x", pady=4)

    # --------------------------------------
    # Clear Main Content
    # --------------------------------------

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # --------------------------------------
    # Get Database Counts
    # --------------------------------------

    def get_count(self, table_name):
        # Only allow known table names in this query.
        allowed_tables = {
            "customers",
            "products",
            "suppliers",
            "employees",
            "sales",
            "purchases"
        }

        if table_name not in allowed_tables:
            return 0

        result = self.database.fetch_one(
            f"SELECT COUNT(*) AS total FROM `{table_name}`"
        )

        return int(result["total"]) if result else 0

    def load_dashboard_counts(self):
        counts = {}

        tables = {
            "Patients": "customers",
            "Medicines": "products",
            "Suppliers": "suppliers",
            "Employees": "employees",
            "Sales": "sales",
            "Purchases": "purchases"
        }

        for label, table_name in tables.items():
            try:
                counts[label] = self.get_count(table_name)
            except Exception as error:
                counts[label] = None
                print(
                    f"Could not load {label} count: {error}"
                )

        return counts

    # --------------------------------------
    # Dashboard Home
    # --------------------------------------

    def show_dashboard(self):
        self.clear_content()

        user = Session.get_user() or {}
        full_name = user.get("full_name", "User")

        header_frame = ttk.Frame(self.content)
        header_frame.pack(fill="x", pady=(10, 5))

        ttk.Label(
            header_frame,
            text="Dashboard",
            font=("Arial", 26, "bold")
        ).pack(side="left")

        ttk.Button(
            header_frame,
            text="Refresh",
            command=self.show_dashboard
        ).pack(side="right", padx=5)

        ttk.Label(
            self.content,
            text=f"Welcome, {full_name}",
            font=("Arial", 15)
        ).pack(anchor="w", pady=(5, 25))

        counts = self.load_dashboard_counts()

        cards_frame = ttk.Frame(self.content)
        cards_frame.pack(fill="x", pady=5)

        card_items = [
            ("Patients", counts["Patients"]),
            ("Medicines", counts["Medicines"]),
            ("Suppliers", counts["Suppliers"]),
            ("Employees", counts["Employees"]),
            ("Sales", counts["Sales"]),
            ("Purchases", counts["Purchases"])
        ]

        for index, (title, value) in enumerate(card_items):
            row = index // 3
            column = index % 3

            card = ttk.LabelFrame(
                cards_frame,
                text=title,
                padding=20
            )
            card.grid(
                row=row,
                column=column,
                padx=8,
                pady=8,
                sticky="nsew"
            )

            display_value = (
                "Error" if value is None else str(value)
            )

            ttk.Label(
                card,
                text=display_value,
                font=("Arial", 24, "bold")
            ).pack(pady=10)

        for column in range(3):
            cards_frame.columnconfigure(
                column,
                weight=1,
                uniform="dashboard_cards"
            )

        ttk.Label(
            self.content,
            text="Counts are loaded from your MySQL database.",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(15, 0))

    # --------------------------------------
    # Patients
    # --------------------------------------

    def show_patients(self):
        self.clear_content()
        CustomerList(self.content)

    # --------------------------------------
    # Medicines
    # --------------------------------------

    def show_medicines(self):
        self.clear_content()
        ProductList(self.content)

    # --------------------------------------
    # Suppliers
    # --------------------------------------

    def show_suppliers(self):
        self.clear_content()
        SupplierList(self.content)

    # --------------------------------------
    # Sales / Billing
    # --------------------------------------

    def show_sales(self):
        self.clear_content()
        SalesList(self.content)

    # --------------------------------------
    # Purchases
    # --------------------------------------

    def show_purchases(self):
        self.clear_content()
        PurchaseList(self.content)

    # --------------------------------------
    # Employees
    # --------------------------------------

    def show_employees(self):
        self.clear_content()
        EmployeeList(self.content)

    # --------------------------------------
    # Reusable Message Page
    # --------------------------------------

    def show_message(self, title, message):
        self.clear_content()

        ttk.Label(
            self.content,
            text=title,
            font=("Arial", 26, "bold")
        ).pack(anchor="w", pady=(10, 20))

        ttk.Label(
            self.content,
            text=message,
            font=("Arial", 14),
            wraplength=750
        ).pack(anchor="w", pady=20)