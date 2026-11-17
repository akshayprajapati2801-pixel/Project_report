
import tkinter as tk
from tkinter import ttk, messagebox

from services.sales_service import SalesService
from ui.sales.sales_form import SalesForm


class SalesList:
    def __init__(self, parent):
        self.parent = parent
        self.service = SalesService()
        self.all_sales = []

        self.frame = ttk.Frame(parent, padding=10)
        self.frame.pack(fill="both", expand=True)

        self.create_widgets()
        self.load_sales()

    def create_widgets(self):
        title = ttk.Label(
            self.frame,
            text="Sales History",
            font=("Arial", 18, "bold")
        )
        title.pack(anchor="w", pady=(0, 10))

        toolbar = ttk.Frame(self.frame)
        toolbar.pack(fill="x", pady=(0, 10))

        ttk.Label(toolbar, text="Search:").pack(side="left", padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            toolbar,
            textvariable=self.search_var,
            width=30
        )
        self.search_entry.pack(side="left", padx=(0, 8))

        self.search_var.trace_add("write", self.filter_sales)

        ttk.Button(
            toolbar,
            text="Add Sale",
            command=self.add_sale
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="View Bill",
            command=self.view_bill
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Edit Sale",
            command=self.edit_sale
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Delete Sale",
            command=self.delete_sale
        ).pack(side="left", padx=3)

        ttk.Button(
            toolbar,
            text="Refresh",
            command=self.load_sales
        ).pack(side="left", padx=3)

        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill="both", expand=True)

        columns = (
            "id",
            "customer_name",
            "total_amount",
            "payment_method",
            "sale_date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=12
        )

        self.tree.heading("id", text="Bill ID")
        self.tree.heading("customer_name", text="Customer")
        self.tree.heading("total_amount", text="Total")
        self.tree.heading("payment_method", text="Payment Method")
        self.tree.heading("sale_date", text="Date")

        self.tree.column("id", width=70, anchor="center")
        self.tree.column("customer_name", width=200)
        self.tree.column("total_amount", width=100, anchor="e")
        self.tree.column("payment_method", width=130)
        self.tree.column("sale_date", width=170)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_sales(self):
        try:
            self.all_sales = self.service.get_all()
            self.filter_sales()
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not load sales history:\n{e}",
                parent=self.frame.winfo_toplevel()
            )

    def filter_sales(self, *_):
        search_text = self.search_var.get().strip().lower()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for sale in self.all_sales:
            bill_id = str(sale.get("id", ""))
            customer = str(sale.get("customer_name", "") or "")
            payment = str(sale.get("payment_method", "") or "")
            sale_date = str(sale.get("sale_date", "") or "")
            total = str(sale.get("total_amount", sale.get("total", "")))

            searchable_text = (
                f"{bill_id} {customer} {payment} {sale_date} {total}"
            ).lower()

            if search_text and search_text not in searchable_text:
                continue

            self.tree.insert(
                "",
                "end",
                values=(
                    bill_id,
                    customer,
                    total,
                    payment,
                    sale_date
                )
            )

    def get_selected_sale_id(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select Sale",
                "Please select a bill first.",
                parent=self.frame.winfo_toplevel()
            )
            return None

        values = self.tree.item(selected[0], "values")

        try:
            return int(values[0])
        except (ValueError, IndexError):
            messagebox.showerror(
                "Error",
                "Could not identify the selected bill.",
                parent=self.frame.winfo_toplevel()
            )
            return None

    def add_sale(self):
        SalesForm(
            self.parent.winfo_toplevel(),
            self.load_sales
        )

    def view_bill(self):
        sale_id = self.get_selected_sale_id()

        if sale_id is None:
            return

        try:
            sale = self.service.get_by_id(sale_id)
            items = self.service.get_sale_items(sale_id)

            if not sale:
                messagebox.showerror(
                    "Not Found",
                    "This bill could not be found.",
                    parent=self.frame.winfo_toplevel()
                )
                return

            details = (
                f"Bill ID: {sale.get('id', '')}\n"
                f"Customer: {sale.get('customer_name', '')}\n"
                f"Date: {sale.get('sale_date', '')}\n"
                f"Payment: {sale.get('payment_method', '')}\n\n"
                "Items:\n"
            )

            for item in items:
                details += (
                    f"- {item.get('product_name', 'Medicine')}: "
                    f"{item.get('quantity', 0)} x "
                    f"{item.get('price', 0)} = "
                    f"{item.get('quantity', 0) * item.get('price', 0)}\n"
                )

            details += (
                f"\nTotal: "
                f"{sale.get('total_amount', sale.get('total', 0))}"
            )

            messagebox.showinfo(
                "Bill Details",
                details,
                parent=self.frame.winfo_toplevel()
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not open bill details:\n{e}",
                parent=self.frame.winfo_toplevel()
            )

    def edit_sale(self):
        sale_id = self.get_selected_sale_id()

        if sale_id is None:
            return

        try:
            sale = self.service.get_by_id(sale_id)

            if not sale:
                messagebox.showerror(
                    "Not Found",
                    "This bill could not be found.",
                    parent=self.frame.winfo_toplevel()
                )
                return

            SalesForm(
                self.parent.winfo_toplevel(),
                self.load_sales,
                sale_id=sale_id
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not edit bill:\n{e}",
                parent=self.frame.winfo_toplevel()
            )

    def delete_sale(self):
        sale_id = self.get_selected_sale_id()

        if sale_id is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete bill #{sale_id}?\n\n"
            "The medicine quantities will be restored to stock.",
            parent=self.frame.winfo_toplevel()
        )

        if not confirm:
            return

        success, message = self.service.delete_sale(sale_id)

        if success:
            messagebox.showinfo(
                "Success",
                message,
                parent=self.frame.winfo_toplevel()
            )
            self.load_sales()
        else:
            messagebox.showerror(
                "Error",
                message,
                parent=self.frame.winfo_toplevel()
            )