
import tkinter as tk
from tkinter import ttk, messagebox

from services.purchase_service import PurchaseService


class PurchaseForm:

    def __init__(
        self,
        parent,
        on_saved=None,
        purchase_id=None
    ):
        self.parent = parent
        self.on_saved = on_saved
        self.purchase_id = purchase_id
        self.is_edit_mode = purchase_id is not None

        self.service = PurchaseService()

        self.products = []
        self.suppliers = []
        self.purchase_items = []

        self.window = tk.Toplevel(parent)
        self.window.title(
            "Edit Purchase" if self.is_edit_mode else "Create Purchase"
        )
        self.window.geometry("850x650")
        self.window.minsize(750, 550)
        self.window.transient(parent)
        self.window.grab_set()

        self.create_ui()
        self.load_data()

    def create_ui(self):
        main_frame = ttk.Frame(self.window, padding=15)
        main_frame.pack(fill="both", expand=True)

        heading = (
            f"Edit Purchase #{self.purchase_id}"
            if self.is_edit_mode
            else "Create Purchase"
        )

        ttk.Label(
            main_frame,
            text=heading,
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(0, 15))

        supplier_frame = ttk.Frame(main_frame)
        supplier_frame.pack(fill="x", pady=5)

        ttk.Label(
            supplier_frame,
            text="Supplier:",
            width=15
        ).pack(side="left")

        self.supplier_var = tk.StringVar()

        self.supplier_combo = ttk.Combobox(
            supplier_frame,
            textvariable=self.supplier_var,
            state="readonly",
            width=40
        )
        self.supplier_combo.pack(side="left", fill="x", expand=True)

        medicine_frame = ttk.LabelFrame(
            main_frame,
            text="Add Medicine",
            padding=10
        )
        medicine_frame.pack(fill="x", pady=10)

        ttk.Label(
            medicine_frame,
            text="Medicine:"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.product_var = tk.StringVar()

        self.product_combo = ttk.Combobox(
            medicine_frame,
            textvariable=self.product_var,
            state="readonly",
            width=35
        )
        self.product_combo.grid(
            row=0, column=1, sticky="ew", padx=5, pady=5
        )
        self.product_combo.bind(
            "<<ComboboxSelected>>",
            self.on_product_selected
        )

        ttk.Label(
            medicine_frame,
            text="Quantity:"
        ).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        self.quantity_var = tk.StringVar(value="1")

        ttk.Entry(
            medicine_frame,
            textvariable=self.quantity_var,
            width=15
        ).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(
            medicine_frame,
            text="Purchase Price:"
        ).grid(row=2, column=0, sticky="w", padx=5, pady=5)

        self.price_var = tk.StringVar()

        ttk.Entry(
            medicine_frame,
            textvariable=self.price_var,
            width=15
        ).grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Button(
            medicine_frame,
            text="Add to Purchase",
            command=self.add_item
        ).grid(
            row=3, column=0, columnspan=2,
            sticky="w", padx=5, pady=10
        )

        medicine_frame.columnconfigure(1, weight=1)

        items_frame = ttk.LabelFrame(
            main_frame,
            text="Purchase Items",
            padding=10
        )
        items_frame.pack(fill="both", expand=True, pady=5)

        columns = (
            "product_id",
            "medicine",
            "quantity",
            "price",
            "subtotal"
        )

        self.tree = ttk.Treeview(
            items_frame,
            columns=columns,
            show="headings",
            height=8,
            selectmode="browse"
        )

        headings = {
            "product_id": "ID",
            "medicine": "Medicine",
            "quantity": "Quantity",
            "price": "Purchase Price",
            "subtotal": "Subtotal"
        }

        widths = {
            "product_id": 50,
            "medicine": 250,
            "quantity": 90,
            "price": 120,
            "subtotal": 120
        }

        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            items_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        ttk.Button(
            items_frame,
            text="Remove Selected Item",
            command=self.remove_item
        ).pack(anchor="w", pady=(8, 0))

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill="x", pady=(10, 0))

        self.total_var = tk.StringVar(value="Total: ₹0.00")

        ttk.Label(
            bottom_frame,
            textvariable=self.total_var,
            font=("Arial", 14, "bold")
        ).pack(side="left")

        ttk.Button(
            bottom_frame,
            text="Save Changes" if self.is_edit_mode else "Save Purchase",
            command=self.save_purchase
        ).pack(side="right", padx=(5, 0))

        ttk.Button(
            bottom_frame,
            text="Cancel",
            command=self.window.destroy
        ).pack(side="right")

    def load_data(self):
        try:
            self.suppliers = self.service.get_suppliers()
            self.products = self.service.get_products()

            self.supplier_map = {}
            self.supplier_ids = {}
            supplier_names = []

            for supplier in self.suppliers:
                name = supplier["name"]
                supplier_id = int(supplier["id"])

                # Include ID so suppliers with the same name
                # can still be distinguished.
                display_name = f"{name} (ID: {supplier_id})"

                self.supplier_map[display_name] = supplier_id
                self.supplier_ids[supplier_id] = display_name
                supplier_names.append(display_name)

            self.supplier_combo["values"] = supplier_names

            self.refresh_product_list()

            if self.is_edit_mode:
                self.load_existing_purchase()
            elif supplier_names:
                self.supplier_combo.current(0)

        except Exception as error:
            messagebox.showerror(
                "Loading Error",
                f"Unable to load purchase data:\n{error}",
                parent=self.window
            )

    def refresh_product_list(self):
        self.product_map = {}
        product_names = []

        for product in self.products:
            if int(product.get("is_active", 1) or 0) != 1:
                continue

            product_id = int(product["id"])
            display_name = f"{product['name']} (ID: {product_id})"

            self.product_map[display_name] = product
            product_names.append(display_name)

        self.product_combo["values"] = product_names

        if product_names:
            self.product_combo.current(0)
            self.on_product_selected()
        else:
            self.product_var.set("")
            self.price_var.set("")

    def load_existing_purchase(self):
        purchase = self.service.get_by_id(self.purchase_id)

        if not purchase:
            messagebox.showerror(
                "Purchase Not Found",
                "The selected purchase could not be found.",
                parent=self.window
            )
            self.window.destroy()
            return

        supplier_id = purchase.get("supplier_id")

        if supplier_id is not None:
            display_name = self.supplier_ids.get(int(supplier_id))

            if display_name:
                self.supplier_var.set(display_name)
            else:
                messagebox.showwarning(
                    "Supplier Unavailable",
                    "The original supplier is no longer in the supplier list. "
                    "Please select an available supplier before saving.",
                    parent=self.window
                )

        existing_items = self.service.get_purchase_items(
            self.purchase_id
        )

        for row in existing_items:
            product_id = int(row["product_id"])
            quantity = int(row["quantity"])
            price = float(row["price"] or 0)

            self.purchase_items.append({
                "product_id": product_id,
                "product_name": row.get("product_name") or (
                    f"Medicine ID {product_id}"
                ),
                "quantity": quantity,
                "price": price,
                "subtotal": quantity * price
            })

        self.refresh_items_table()

    def on_product_selected(self, event=None):
        display_name = self.product_var.get()
        product = self.product_map.get(display_name)

        if product:
            purchase_price = product.get("purchase_price")
            self.price_var.set(str(float(purchase_price or 0)))

    def add_item(self):
        display_name = self.product_var.get()
        product = self.product_map.get(display_name)

        if not product:
            messagebox.showwarning(
                "Medicine Required",
                "Please select an active medicine.",
                parent=self.window
            )
            return

        try:
            latest_product = self.service.get_product_by_id(
                product["id"]
            )
        except Exception as error:
            messagebox.showerror(
                "Medicine Error",
                f"Unable to verify medicine:\n{error}",
                parent=self.window
            )
            return

        if not latest_product:
            messagebox.showerror(
                "Medicine Error",
                "This medicine no longer exists.",
                parent=self.window
            )
            return

        if int(latest_product.get("is_active", 1) or 0) != 1:
            messagebox.showerror(
                "Inactive Medicine",
                "This medicine is inactive. Please select an active medicine.",
                parent=self.window
            )
            return

        try:
            quantity = int(self.quantity_var.get().strip())
            price = float(self.price_var.get().strip())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Quantity must be a whole number and price must be numeric.",
                parent=self.window
            )
            return

        if quantity <= 0:
            messagebox.showerror(
                "Invalid Quantity",
                "Quantity must be greater than zero.",
                parent=self.window
            )
            return

        if price < 0:
            messagebox.showerror(
                "Invalid Price",
                "Purchase price cannot be negative.",
                parent=self.window
            )
            return

        product_id = int(latest_product["id"])

        for item in self.purchase_items:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                item["price"] = price
                item["subtotal"] = item["quantity"] * price
                self.refresh_items_table()
                self.quantity_var.set("1")
                return

        self.purchase_items.append({
            "product_id": product_id,
            "product_name": latest_product["name"],
            "quantity": quantity,
            "price": price,
            "subtotal": quantity * price
        })

        self.refresh_items_table()
        self.quantity_var.set("1")

    def refresh_items_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0

        for item in self.purchase_items:
            item["subtotal"] = item["quantity"] * item["price"]
            total += item["subtotal"]

            self.tree.insert(
                "",
                "end",
                values=(
                    item["product_id"],
                    item["product_name"],
                    item["quantity"],
                    f"₹{item['price']:.2f}",
                    f"₹{item['subtotal']:.2f}"
                )
            )

        self.total_var.set(f"Total: ₹{total:.2f}")

    def remove_item(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection Required",
                "Please select an item to remove.",
                parent=self.window
            )
            return

        values = self.tree.item(selected[0], "values")
        product_id = int(values[0])

        self.purchase_items = [
            item for item in self.purchase_items
            if item["product_id"] != product_id
        ]

        self.refresh_items_table()

    def save_purchase(self):
        supplier_name = self.supplier_var.get()
        supplier_id = self.supplier_map.get(supplier_name)

        if supplier_id is None:
            messagebox.showwarning(
                "Supplier Required",
                "Please select a valid supplier.",
                parent=self.window
            )
            return

        if not self.purchase_items:
            messagebox.showwarning(
                "Items Required",
                "Please add at least one medicine.",
                parent=self.window
            )
            return

        action = "update" if self.is_edit_mode else "save"

        confirm = messagebox.askyesno(
            "Confirm Changes" if self.is_edit_mode else "Confirm Purchase",
            f"Are you sure you want to {action} this purchase?\n\n"
            f"{self.total_var.get()}",
            parent=self.window
        )

        if not confirm:
            return

        if self.is_edit_mode:
            success, message = self.service.update_purchase(
                self.purchase_id,
                supplier_id,
                self.purchase_items
            )
        else:
            success, message = self.service.create_purchase(
                supplier_id,
                self.purchase_items
            )

        if not success:
            messagebox.showerror(
                "Purchase Error",
                message,
                parent=self.window
            )
            return

        messagebox.showinfo(
            "Success",
            message,
            parent=self.window
        )

        if self.on_saved:
            self.on_saved()

        self.window.destroy()