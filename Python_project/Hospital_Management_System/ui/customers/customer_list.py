import tkinter as tk
from tkinter import ttk, messagebox

from services.customer_service import CustomerService
from ui.customers.customer_form import CustomerForm


class CustomerList:

    def __init__(self, parent):

        self.parent = parent
        self.service = CustomerService()

        self.customers = []

        self.create_ui()
        self.load_customers()

    def create_ui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()

        # Header
        header = ttk.Frame(self.parent)
        header.pack(
            fill="x",
            pady=(0, 15)
        )

        title = ttk.Label(
            header,
            text="Patients",
            font=("Arial", 26, "bold")
        )

        title.pack(
            side="left"
        )

        ttk.Button(
            header,
            text="+ Add Patient",
            command=self.add_customer
        ).pack(
            side="right"
        )

        # Search
        search_frame = ttk.Frame(
            self.parent
        )

        search_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        ttk.Label(
            search_frame,
            text="Search Patient:"
        ).pack(
            side="left"
        )

        self.search_entry = ttk.Entry(
            search_frame,
            width=35
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_customers
        )

        ttk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search
        ).pack(
            side="left"
        )

        # Table
        table_frame = ttk.Frame(
            self.parent
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical"
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        columns = (
            "id",
            "name",
            "phone",
            "email",
            "age",
            "gender",
            "address"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(
            command=self.tree.yview
        )

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "name",
            text="Patient Name"
        )

        self.tree.heading(
            "phone",
            text="Phone"
        )

        self.tree.heading(
            "email",
            text="Email"
        )

        self.tree.heading(
            "age",
            text="Age"
        )

        self.tree.heading(
            "gender",
            text="Gender"
        )

        self.tree.heading(
            "address",
            text="Address"
        )

        self.tree.column(
            "id",
            width=60
        )

        self.tree.column(
            "name",
            width=180
        )

        self.tree.column(
            "phone",
            width=130
        )

        self.tree.column(
            "email",
            width=190
        )

        self.tree.column(
            "age",
            width=70
        )

        self.tree.column(
            "gender",
            width=100
        )

        self.tree.column(
            "address",
            width=220
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        # Buttons
        buttons_frame = ttk.Frame(
            self.parent
        )

        buttons_frame.pack(
            fill="x",
            pady=15
        )

        ttk.Button(
            buttons_frame,
            text="Add Patient",
            command=self.add_customer
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Edit Patient",
            command=self.edit_customer
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Delete Patient",
            command=self.delete_customer
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.load_customers
        ).pack(
            side="left",
            padx=5
        )

    def load_customers(self):

        try:

            self.customers = (
                self.service.get_all()
            )

            self.display_customers(
                self.customers
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def display_customers(self, customers):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for customer in customers:

            self.tree.insert(
                "",
                "end",
                values=(
                    customer["id"],
                    customer["name"],
                    customer["phone"] or "",
                    customer["email"] or "",
                    customer["age"] or "",
                    customer["gender"] or "",
                    customer["address"] or ""
                )
            )

    def search_customers(self, event=None):

        search_text = (
            self.search_entry
            .get()
            .strip()
            .lower()
        )

        if not search_text:

            self.display_customers(
                self.customers
            )

            return

        filtered_customers = []

        for customer in self.customers:

            name = (
                customer["name"]
                or ""
            ).lower()

            phone = (
                customer["phone"]
                or ""
            ).lower()

            email = (
                customer["email"]
                or ""
            ).lower()

            gender = (
                customer["gender"]
                or ""
            ).lower()

            if (
                search_text in name
                or search_text in phone
                or search_text in email
                or search_text in gender
            ):

                filtered_customers.append(
                    customer
                )

        self.display_customers(
            filtered_customers
        )

    def clear_search(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.display_customers(
            self.customers
        )

    def add_customer(self):

        CustomerForm(
            self.parent.winfo_toplevel(),
            self.load_customers
        )

    def get_selected_customer(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Selection Required",
                "Please select a patient."
            )

            return None

        item = self.tree.item(
            selected[0]
        )

        customer_id = item["values"][0]

        try:

            return self.service.get_by_id(
                customer_id
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return None

    def edit_customer(self):

        customer = self.get_selected_customer()

        if customer is None:
            return

        CustomerForm(
            self.parent.winfo_toplevel(),
            self.load_customers,
            customer
        )

    def delete_customer(self):

        customer = self.get_selected_customer()

        if customer is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete "
            f"'{customer['name']}'?"
        )

        if not confirm:
            return

        success, message = (
            self.service.delete(
                customer["id"]
            )
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.load_customers()

        else:

            messagebox.showerror(
                "Delete Failed",
                message
            )