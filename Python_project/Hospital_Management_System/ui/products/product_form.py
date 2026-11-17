
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from services.product_service import ProductService


class ProductForm:

    def __init__(self, parent, product=None, on_saved=None):
        self.parent = parent
        self.product = product
        self.on_saved = on_saved
        self.service = ProductService()

        self.window = tk.Toplevel(parent)
        self.window.title(
            "Edit Medicine" if product else "Add Medicine"
        )
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self.create_ui()

        if self.product:
            self.fill_form()

    def create_ui(self):
        main = ttk.Frame(self.window, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main,
            text="Edit Medicine" if self.product else "Add Medicine",
            font=("Arial", 18, "bold")
        ).pack(anchor="w", pady=(0, 20))

        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.purchase_price_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.supplier_var = tk.StringVar()
        self.expiry_date_var = tk.StringVar()

        self.create_field(main, "Medicine Name", self.name_var)
        self.create_field(main, "Category", self.category_var)
        self.create_field(main, "Selling Price", self.price_var)
        self.create_field(main, "Purchase Price", self.purchase_price_var)
        self.create_field(main, "Quantity", self.quantity_var)

        ttk.Label(main, text="Supplier").pack(anchor="w", pady=(10, 3))

        self.supplier_combo = ttk.Combobox(
            main,
            textvariable=self.supplier_var,
            state="readonly"
        )
        self.supplier_combo.pack(fill="x")

        ttk.Label(
            main,
            text="Expiry Date (YYYY-MM-DD; optional)"
        ).pack(anchor="w", pady=(10, 3))

        ttk.Entry(
            main,
            textvariable=self.expiry_date_var
        ).pack(fill="x")

        ttk.Label(
            main,
            text="Example: 2027-12-31",
            foreground="gray"
        ).pack(anchor="w", pady=(3, 0))

        self.load_suppliers()

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=(25, 0))

        ttk.Button(
            buttons,
            text="Save",
            command=self.save
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            buttons,
            text="Cancel",
            command=self.window.destroy
        ).pack(side="left")

    def create_field(self, parent, label_text, variable):
        ttk.Label(
            parent,
            text=label_text
        ).pack(anchor="w", pady=(8, 3))

        ttk.Entry(
            parent,
            textvariable=variable
        ).pack(fill="x")

    def load_suppliers(self):
        try:
            self.suppliers = self.service.get_suppliers()

            self.supplier_combo["values"] = [
                supplier["name"] for supplier in self.suppliers
            ]

            if self.suppliers and not self.product:
                self.supplier_combo.current(0)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Unable to load suppliers:\n{error}",
                parent=self.window
            )

    def fill_form(self):
        self.name_var.set(self.product.get("name") or "")
        self.category_var.set(self.product.get("category") or "")
        self.price_var.set(str(self.product.get("price", 0)))
        self.purchase_price_var.set(
            str(self.product.get("purchase_price", 0))
        )
        self.quantity_var.set(str(self.product.get("quantity", 0)))

        expiry = self.product.get("expiry_date")
        self.expiry_date_var.set(
            expiry.strftime("%Y-%m-%d")
            if expiry and hasattr(expiry, "strftime")
            else str(expiry or "")
        )

        supplier_id = self.product.get("supplier_id")

        for index, supplier in enumerate(self.suppliers):
            if supplier["id"] == supplier_id:
                self.supplier_combo.current(index)
                break

    def save(self):
        name = self.name_var.get().strip()
        category = self.category_var.get().strip()
        expiry_text = self.expiry_date_var.get().strip()

        if not name:
            messagebox.showwarning(
                "Validation",
                "Medicine name is required.",
                parent=self.window
            )
            return

        try:
            price = float(self.price_var.get())
            purchase_price = float(self.purchase_price_var.get())
            quantity = int(self.quantity_var.get())

            if price < 0 or purchase_price < 0 or quantity < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter valid non-negative prices and a whole-number quantity.",
                parent=self.window
            )
            return

        expiry_date = None

        if expiry_text:
            try:
                expiry_date = date.fromisoformat(expiry_text)
            except ValueError:
                messagebox.showerror(
                    "Invalid Date",
                    "Enter the expiry date in YYYY-MM-DD format, e.g. 2027-12-31.",
                    parent=self.window
                )
                return

        supplier_index = self.supplier_combo.current()
        supplier_id = (
            self.suppliers[supplier_index]["id"]
            if supplier_index >= 0 else None
        )

        try:
            if self.product:
                success, message = self.service.update(
                    self.product["id"],
                    name,
                    category,
                    price,
                    purchase_price,
                    quantity,
                    supplier_id,
                    expiry_date
                )
            else:
                success, message = self.service.create(
                    name,
                    category,
                    price,
                    purchase_price,
                    quantity,
                    supplier_id,
                    expiry_date
                )

            if success:
                messagebox.showinfo(
                    "Success",
                    message,
                    parent=self.window
                )

                if self.on_saved:
                    self.on_saved()

                self.window.destroy()
            else:
                messagebox.showerror(
                    "Error",
                    message,
                    parent=self.window
                )

        except Exception as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.window
            )