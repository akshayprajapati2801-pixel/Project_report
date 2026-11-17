
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta

from services.product_service import ProductService
from ui.products.product_form import ProductForm


class ProductList:

    def __init__(self, parent):
        self.parent = parent
        self.service = ProductService()
        self.products = []

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.create_ui()
        self.load_products()

    def create_ui(self):
        header = ttk.Frame(self.frame)
        header.pack(fill="x", padx=20, pady=(20, 10))

        ttk.Label(
            header,
            text="Medicines",
            font=("Arial", 20, "bold")
        ).pack(side="left")

        ttk.Button(
            header,
            text="Add Medicine",
            command=self.add_product
        ).pack(side="right")

        search_frame = ttk.Frame(self.frame)
        search_frame.pack(fill="x", padx=20, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side="left")

        self.search_var = tk.StringVar()

        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=40
        )
        search_entry.pack(side="left", padx=10)
        search_entry.bind(
            "<KeyRelease>",
            lambda event: self.filter_products()
        )

        ttk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search
        ).pack(side="left")

        ttk.Label(
            self.frame,
            text=(
                "Low stock: quantity 10 or below | "
                "Expiring soon: within 30 days"
            ),
            font=("Arial", 10)
        ).pack(anchor="w", padx=20, pady=5)

        table_frame = ttk.Frame(self.frame)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "id",
            "name",
            "category",
            "selling_price",
            "purchase_price",
            "quantity",
            "stock_status",
            "expiry_date",
            "supplier",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "id": "ID",
            "name": "Medicine",
            "category": "Category",
            "selling_price": "Selling Price",
            "purchase_price": "Purchase Price",
            "quantity": "Quantity",
            "stock_status": "Stock Status",
            "expiry_date": "Expiry Date",
            "supplier": "Supplier",
            "status": "Status"
        }

        widths = {
            "id": 40,
            "name": 125,
            "category": 85,
            "selling_price": 100,
            "purchase_price": 100,
            "quantity": 60,
            "stock_status": 100,
            "expiry_date": 100,
            "supplier": 120,
            "status": 75
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        self.tree.tag_configure(
            "low_stock",
            background="light yellow"
        )
        self.tree.tag_configure(
            "out_of_stock",
            foreground="red"
        )
        self.tree.tag_configure(
            "expired",
            foreground="red"
        )
        self.tree.tag_configure(
            "expiring_soon",
            foreground="#C77700"
        )
        self.tree.tag_configure(
            "valid",
            foreground="green"
        )
        self.tree.tag_configure(
            "no_expiry",
            foreground="gray"
        )
        self.tree.tag_configure(
            "inactive",
            background="#E5E5E5",
            foreground="#666666"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))

        ttk.Button(
            button_frame,
            text="Edit",
            command=self.edit_product
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_product
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Deactivate",
            command=self.deactivate_product
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Activate",
            command=self.activate_product
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Refresh",
            command=self.load_products
        ).pack(side="left", padx=5)

    def load_products(self):
        try:
            self.products = self.service.get_all()
            self.filter_products()
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Unable to load medicines:\n{error}"
            )

    def filter_products(self):
        search_text = self.search_var.get().strip().lower()

        for item in self.tree.get_children():
            self.tree.delete(item)

        today = date.today()
        soon_limit = today + timedelta(days=30)

        for product in self.products:
            name = str(product.get("name") or "").lower()
            category = str(product.get("category") or "").lower()
            supplier = str(product.get("supplier_name") or "").lower()

            if search_text and search_text not in (
                f"{name} {category} {supplier}"
            ):
                continue

            quantity = int(product.get("quantity") or 0)

            if quantity <= 0:
                stock_status = "Out of Stock"
                stock_tag = "out_of_stock"
            elif quantity <= 10:
                stock_status = "Low Stock"
                stock_tag = "low_stock"
            else:
                stock_status = "In Stock"
                stock_tag = ""

            expiry = product.get("expiry_date")
            expiry_text = "Not Set"
            expiry_tag = "no_expiry"

            if expiry:
                if isinstance(expiry, str):
                    try:
                        expiry = date.fromisoformat(expiry[:10])
                    except ValueError:
                        expiry = None

                if isinstance(expiry, date):
                    expiry_text = expiry.strftime("%Y-%m-%d")

                    if expiry < today:
                        expiry_tag = "expired"
                    elif expiry <= soon_limit:
                        expiry_tag = "expiring_soon"
                    else:
                        expiry_tag = "valid"

            is_active = int(product.get("is_active", 1) or 0)
            status_text = "Active" if is_active else "Inactive"

            values = (
                product.get("id"),
                product.get("name"),
                product.get("category"),
                f"₹{float(product.get('price') or 0):.2f}",
                f"₹{float(product.get('purchase_price') or 0):.2f}",
                quantity,
                stock_status,
                expiry_text,
                product.get("supplier_name") or "Not Assigned",
                status_text
            )

            tags = [expiry_tag]

            if stock_tag:
                tags.append(stock_tag)

            if not is_active:
                tags = ["inactive"]

            self.tree.insert(
                "",
                "end",
                values=values,
                tags=tuple(tags)
            )

    def clear_search(self):
        self.search_var.set("")
        self.filter_products()

    def get_selected_product(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection",
                "Please select a medicine first."
            )
            return None

        values = self.tree.item(selected[0], "values")
        product_id = int(values[0])

        for product in self.products:
            if int(product["id"]) == product_id:
                return product

        return None

    def add_product(self):
        ProductForm(self.parent, on_saved=self.load_products)

    def edit_product(self):
        product = self.get_selected_product()

        if product:
            ProductForm(
                self.parent,
                product=product,
                on_saved=self.load_products
            )

    def deactivate_product(self):
        product = self.get_selected_product()

        if not product:
            return

        if not int(product.get("is_active", 1) or 0):
            messagebox.showinfo(
                "Already Inactive",
                "This medicine is already inactive."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Deactivation",
            f"Deactivate '{product['name']}'?\n\n"
            "It will remain in your records, but should not be sold."
        )

        if not confirm:
            return

        success, message = self.service.set_active_status(
            product["id"],
            False
        )

        if success:
            messagebox.showinfo("Success", message)
            self.load_products()
        else:
            messagebox.showerror("Error", message)

    def activate_product(self):
        product = self.get_selected_product()

        if not product:
            return

        if int(product.get("is_active", 1) or 0):
            messagebox.showinfo(
                "Already Active",
                "This medicine is already active."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Activation",
            f"Activate '{product['name']}'?"
        )

        if not confirm:
            return

        success, message = self.service.set_active_status(
            product["id"],
            True
        )

        if success:
            messagebox.showinfo("Success", message)
            self.load_products()
        else:
            messagebox.showerror("Error", message)

    def delete_product(self):
        product = self.get_selected_product()

        if not product:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete medicine '{product['name']}'?"
        )

        if not confirm:
            return

        success, message = self.service.delete(product["id"])

        if success:
            messagebox.showinfo("Success", message)
            self.load_products()
        else:
            messagebox.showerror("Error", message)