
import tkinter as tk
from tkinter import ttk, messagebox

from services.purchase_service import PurchaseService
from ui.purchases.purchase_form import PurchaseForm


class PurchaseList:

    def __init__(self, parent):
        self.parent = parent
        self.service = PurchaseService()
        self.purchases = []

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.create_ui()
        self.load_purchases()

    def create_ui(self):
        # Page heading and buttons
        header = ttk.Frame(self.frame)
        header.pack(fill="x", padx=20, pady=(20, 10))

        ttk.Label(
            header,
            text="Purchase History",
            font=("Arial", 20, "bold")
        ).pack(side="left")

        ttk.Button(
            header,
            text="Refresh",
            command=self.load_purchases
        ).pack(side="right", padx=(5, 0))

        ttk.Button(
            header,
            text="Add Purchase",
            command=self.add_purchase
        ).pack(side="right", padx=(5, 0))

        ttk.Label(
            self.frame,
            text="Select a purchase to view details, edit, or delete it.",
            font=("Arial", 10)
        ).pack(anchor="w", padx=20, pady=5)

        # Purchase history table
        table_frame = ttk.LabelFrame(
            self.frame,
            text="Saved Purchases",
            padding=10
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = ("id", "supplier", "date", "total")

        self.purchase_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=9,
            selectmode="browse"
        )

        headings = {
            "id": "Purchase ID",
            "supplier": "Supplier",
            "date": "Purchase Date",
            "total": "Total Amount"
        }

        widths = {
            "id": 100,
            "supplier": 250,
            "date": 180,
            "total": 150
        }

        for column in columns:
            self.purchase_tree.heading(
                column,
                text=headings[column]
            )
            self.purchase_tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        purchase_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.purchase_tree.yview
        )

        self.purchase_tree.configure(
            yscrollcommand=purchase_scrollbar.set
        )

        self.purchase_tree.pack(
            side="left",
            fill="both",
            expand=True
        )
        purchase_scrollbar.pack(side="right", fill="y")

        self.purchase_tree.bind(
            "<<TreeviewSelect>>",
            self.on_purchase_selected
        )

        # Purchase action buttons
        action_frame = ttk.Frame(self.frame)
        action_frame.pack(fill="x", padx=20, pady=(0, 10))

        ttk.Button(
            action_frame,
            text="View Details",
            command=self.on_purchase_selected
        ).pack(side="left", padx=(0, 5))

        ttk.Button(
            action_frame,
            text="Edit Purchase",
            command=self.edit_purchase
        ).pack(side="left", padx=5)

        ttk.Button(
            action_frame,
            text="Delete Purchase",
            command=self.delete_purchase
        ).pack(side="left", padx=5)

        # Selected purchase medicine details
        details_frame = ttk.LabelFrame(
            self.frame,
            text="Medicine Details",
            padding=10
        )
        details_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 10)
        )

        detail_columns = (
            "product_id",
            "medicine",
            "quantity",
            "price",
            "subtotal"
        )

        self.items_tree = ttk.Treeview(
            details_frame,
            columns=detail_columns,
            show="headings",
            height=6
        )

        detail_headings = {
            "product_id": "Medicine ID",
            "medicine": "Medicine Name",
            "quantity": "Quantity",
            "price": "Purchase Price",
            "subtotal": "Subtotal"
        }

        detail_widths = {
            "product_id": 90,
            "medicine": 230,
            "quantity": 90,
            "price": 130,
            "subtotal": 130
        }

        for column in detail_columns:
            self.items_tree.heading(
                column,
                text=detail_headings[column]
            )
            self.items_tree.column(
                column,
                width=detail_widths[column],
                anchor="center"
            )

        items_scrollbar = ttk.Scrollbar(
            details_frame,
            orient="vertical",
            command=self.items_tree.yview
        )

        self.items_tree.configure(
            yscrollcommand=items_scrollbar.set
        )

        self.items_tree.pack(
            side="left",
            fill="both",
            expand=True
        )
        items_scrollbar.pack(side="right", fill="y")

        # Footer
        footer = ttk.Frame(self.frame)
        footer.pack(fill="x", padx=20, pady=(0, 20))

        self.count_var = tk.StringVar(
            value="Total purchases: 0"
        )

        ttk.Label(
            footer,
            textvariable=self.count_var
        ).pack(side="left")

        self.details_total_var = tk.StringVar(
            value="Selected purchase: ₹0.00"
        )

        ttk.Label(
            footer,
            textvariable=self.details_total_var,
            font=("Arial", 12, "bold")
        ).pack(side="right")

    def get_selected_purchase_id(self):
        selected = self.purchase_tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Purchase Selected",
                "Please select a purchase from the history table first.",
                parent=self.window_parent()
            )
            return None

        values = self.purchase_tree.item(
            selected[0],
            "values"
        )

        try:
            return int(values[0])
        except (ValueError, IndexError, TypeError):
            messagebox.showerror(
                "Selection Error",
                "The selected purchase ID is invalid.",
                parent=self.window_parent()
            )
            return None

    def window_parent(self):
        return self.frame.winfo_toplevel()

    def add_purchase(self):
        PurchaseForm(
            self.parent,
            on_saved=self.load_purchases
        )

    def edit_purchase(self):
        purchase_id = self.get_selected_purchase_id()

        if purchase_id is None:
            return

        purchase = self.service.get_by_id(purchase_id)

        if not purchase:
            messagebox.showerror(
                "Purchase Not Found",
                "The selected purchase could not be found.",
                parent=self.window_parent()
            )
            self.load_purchases()
            return

        PurchaseForm(
            self.parent,
            on_saved=self.load_purchases,
            purchase_id=purchase_id
        )

    def delete_purchase(self):
        purchase_id = self.get_selected_purchase_id()

        if purchase_id is None:
            return

        confirmed = messagebox.askyesno(
            "Confirm Purchase Deletion",
            f"Are you sure you want to delete Purchase #{purchase_id}?\n\n"
            "The application will attempt to reverse the quantities "
            "added by this purchase.\n\n"
            "Deletion will be blocked if there is insufficient stock "
            "to reverse the original quantities.\n\n"
            "This action cannot be undone.",
            icon="warning",
            parent=self.window_parent()
        )

        if not confirmed:
            return

        success, message = self.service.delete_purchase(purchase_id)

        if success:
            messagebox.showinfo(
                "Purchase Deleted",
                message,
                parent=self.window_parent()
            )
            self.load_purchases()
        else:
            messagebox.showerror(
                "Deletion Failed",
                message,
                parent=self.window_parent()
            )

    def load_purchases(self):
        try:
            self.purchases = self.service.get_all()

            for row in self.purchase_tree.get_children():
                self.purchase_tree.delete(row)

            self.clear_items()

            for purchase in self.purchases:
                purchase_date = purchase.get("purchase_date")

                date_text = (
                    str(purchase_date)
                    if purchase_date is not None
                    else "N/A"
                )

                total = float(purchase.get("total") or 0)

                self.purchase_tree.insert(
                    "",
                    "end",
                    values=(
                        purchase.get("id"),
                        purchase.get("supplier_name") or "Unknown",
                        date_text,
                        f"₹{total:.2f}"
                    )
                )

            self.count_var.set(
                f"Total purchases: {len(self.purchases)}"
            )

        except Exception as error:
            messagebox.showerror(
                "Loading Error",
                f"Unable to load purchase history:\n{error}",
                parent=self.window_parent()
            )

    def on_purchase_selected(self, event=None):
        selected = self.purchase_tree.selection()

        if not selected:
            if event is None:
                messagebox.showwarning(
                    "No Purchase Selected",
                    "Please select a purchase first.",
                    parent=self.window_parent()
                )
            return

        values = self.purchase_tree.item(
            selected[0],
            "values"
        )

        try:
            purchase_id = int(values[0])
            items = self.service.get_purchase_items(purchase_id)

            self.clear_items()
            total = 0

            for item in items:
                quantity = int(item.get("quantity") or 0)
                price = float(item.get("price") or 0)
                subtotal = float(item.get("subtotal") or 0)

                total += subtotal

                self.items_tree.insert(
                    "",
                    "end",
                    values=(
                        item.get("product_id"),
                        item.get("product_name") or "Medicine unavailable",
                        quantity,
                        f"₹{price:.2f}",
                        f"₹{subtotal:.2f}"
                    )
                )

            self.details_total_var.set(
                f"Selected purchase: ₹{total:.2f}"
            )

        except Exception as error:
            messagebox.showerror(
                "Details Error",
                f"Unable to load purchase details:\n{error}",
                parent=self.window_parent()
            )

    def clear_items(self):
        for row in self.items_tree.get_children():
            self.items_tree.delete(row)

        self.details_total_var.set(
            "Selected purchase: ₹0.00"
        )