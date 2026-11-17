
import tkinter as tk
from tkinter import ttk, messagebox

from services.sales_service import SalesService


class SalesForm:

    def __init__(self, parent, on_saved, sale_id=None):
        self.parent = parent
        self.on_saved = on_saved
        self.sale_id = sale_id
        self.is_editing = sale_id is not None

        self.service = SalesService()
        self.customers = []
        self.products = []
        self.cart = []

        self.window = tk.Toplevel(parent)
        self.window.title("Edit Bill" if self.is_editing else "Create Bill")
        self.window.geometry("900x700")
        self.window.resizable(False, False)

        self.create_form()
        self.load_customers()
        self.load_products()

        if self.is_editing:
            self.load_existing_sale()

    def create_form(self):
        main_frame = ttk.Frame(self.window, padding=20)
        main_frame.pack(fill="both", expand=True)

        self.title_label = ttk.Label(
            main_frame,
            text="Edit Bill" if self.is_editing else "Create Bill",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=(0, 15))

        customer_frame = ttk.Frame(main_frame)
        customer_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(customer_frame, text="Customer").pack(anchor="w")

        self.customer_combo = ttk.Combobox(
            customer_frame, state="readonly", width=40
        )
        self.customer_combo.pack(anchor="w", pady=5)

        medicine_frame = ttk.LabelFrame(
            main_frame, text="Add Medicine", padding=12
        )
        medicine_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(medicine_frame, text="Medicine").grid(
            row=0, column=0, sticky="w", padx=5
        )
        self.product_combo = ttk.Combobox(
            medicine_frame, state="readonly", width=35
        )
        self.product_combo.grid(row=1, column=0, padx=5, pady=5)
        self.product_combo.bind(
            "<<ComboboxSelected>>", self.on_product_selected
        )

        ttk.Label(medicine_frame, text="Quantity").grid(
            row=0, column=1, sticky="w", padx=5
        )
        self.quantity_entry = ttk.Entry(medicine_frame, width=12)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(medicine_frame, text="Selling Price").grid(
            row=0, column=2, sticky="w", padx=5
        )
        self.price_entry = ttk.Entry(medicine_frame, width=15)
        self.price_entry.grid(row=1, column=2, padx=5, pady=5)

        ttk.Button(
            medicine_frame,
            text="Add to Bill",
            command=self.add_to_cart
        ).grid(row=1, column=3, padx=10, pady=5)

        cart_frame = ttk.Frame(main_frame)
        cart_frame.pack(fill="both", expand=True, pady=(0, 5))

        columns = ("medicine", "price", "quantity", "subtotal")
        self.cart_tree = ttk.Treeview(
            cart_frame, columns=columns, show="headings", height=8
        )

        self.cart_tree.heading("medicine", text="Medicine")
        self.cart_tree.heading("price", text="Selling Price")
        self.cart_tree.heading("quantity", text="Quantity")
        self.cart_tree.heading("subtotal", text="Subtotal")

        self.cart_tree.column("medicine", width=320)
        self.cart_tree.column("price", width=150)
        self.cart_tree.column("quantity", width=120)
        self.cart_tree.column("subtotal", width=150)
        self.cart_tree.pack(fill="both", expand=True)

        ttk.Button(
            main_frame,
            text="Remove Selected",
            command=self.remove_from_cart
        ).pack(anchor="w", pady=5)

        payment_frame = ttk.Frame(main_frame)
        payment_frame.pack(fill="x", pady=5)

        ttk.Label(payment_frame, text="Payment Method").pack(side="left")

        self.payment_combo = ttk.Combobox(
            payment_frame,
            state="readonly",
            values=["Cash", "Card", "UPI"],
            width=15
        )
        self.payment_combo.pack(side="left", padx=10)
        self.payment_combo.set("Cash")

        self.total_label = ttk.Label(
            main_frame,
            text="Total: ₹0.00",
            font=("Arial", 18, "bold")
        )
        self.total_label.pack(anchor="e", pady=5)

        ttk.Button(
            main_frame,
            text="UPDATE BILL" if self.is_editing else "SAVE BILL",
            command=self.save_sale
        ).pack(pady=8)

    def load_customers(self):
        try:
            self.customers = self.service.get_customers()
            self.customer_combo["values"] = [
                customer["name"] for customer in self.customers
            ]
        except Exception as error:
            messagebox.showerror(
                "Database Error", str(error), parent=self.window
            )

    def load_products(self):
        try:
            self.products = self.service.get_products()
            self.product_combo["values"] = [
                product["name"] for product in self.products
            ]
        except Exception as error:
            messagebox.showerror(
                "Database Error", str(error), parent=self.window
            )

    def load_existing_sale(self):
        try:
            sale = self.service.get_by_id(self.sale_id)
            if not sale:
                messagebox.showerror(
                    "Not Found", "This bill could not be found.",
                    parent=self.window
                )
                self.window.destroy()
                return

            customer_id = sale.get("customer_id")
            for index, customer in enumerate(self.customers):
                if customer["id"] == customer_id:
                    self.customer_combo.current(index)
                    break

            payment_method = sale.get("payment_method") or "Cash"
            if payment_method in self.payment_combo["values"]:
                self.payment_combo.set(payment_method)
            else:
                self.payment_combo.set("Cash")

            existing_items = self.service.get_sale_items(self.sale_id)

            for row in existing_items:
                product_id = row.get("product_id")
                product = next(
                    (p for p in self.products if p["id"] == product_id),
                    None
                )

                # Existing sold medicines may now be inactive or expired.
                # Preserve their saved details so the bill can be reviewed.
                self.cart.append({
                    "product_id": product_id,
                    "product_name": (
                        row.get("product_name") or f"Medicine #{product_id}"
                    ),
                    "quantity": int(row["quantity"]),
                    "price": float(row["price"]),
                    "subtotal": float(row["subtotal"]),
                    "available_stock": (
                        int(product["quantity"]) if product else 0
                    )
                })

            self.refresh_cart()

        except Exception as error:
            messagebox.showerror(
                "Load Error", str(error), parent=self.window
            )

    def on_product_selected(self, event=None):
        product = self.get_selected_product()
        if product is None:
            return

        self.price_entry.delete(0, tk.END)
        self.price_entry.insert(0, str(product["price"]))

    def get_selected_customer_id(self):
        selected = self.customer_combo.get()
        for customer in self.customers:
            if customer["name"] == selected:
                return customer["id"]
        return None

    def get_selected_product(self):
        selected = self.product_combo.get()
        for product in self.products:
            if product["name"] == selected:
                return product
        return None

    def add_to_cart(self):
        product = self.get_selected_product()
        if product is None:
            messagebox.showwarning(
                "Medicine Required", "Please select a medicine.",
                parent=self.window
            )
            return

        try:
            quantity = int(self.quantity_entry.get())
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Enter a whole-number quantity and a valid price.",
                parent=self.window
            )
            return

        if quantity <= 0:
            messagebox.showerror(
                "Invalid Quantity", "Quantity must be greater than zero.",
                parent=self.window
            )
            return

        if price < 0:
            messagebox.showerror(
                "Invalid Price", "Price cannot be negative.",
                parent=self.window
            )
            return

        existing_item = next(
            (item for item in self.cart
             if item["product_id"] == product["id"]),
            None
        )

        new_quantity = quantity
        if existing_item:
            new_quantity += existing_item["quantity"]

        # In edit mode, current stock excludes the quantity already
        # deducted by this bill. Add that quantity back for validation.
        old_quantity = 0
        if self.is_editing:
            for row in self.service.get_sale_items(self.sale_id):
                if row["product_id"] == product["id"]:
                    old_quantity += int(row["quantity"])

        allowed_quantity = int(product["quantity"]) + old_quantity

        if new_quantity > allowed_quantity:
            messagebox.showerror(
                "Insufficient Stock",
                f"Available for this bill: {allowed_quantity} units.",
                parent=self.window
            )
            return

        if existing_item:
            existing_item["quantity"] = new_quantity
            existing_item["price"] = price
            existing_item["subtotal"] = new_quantity * price
        else:
            self.cart.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "quantity": quantity,
                "price": price,
                "subtotal": quantity * price
            })

        self.refresh_cart()
        self.quantity_entry.delete(0, tk.END)

    def refresh_cart(self):
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        total = 0.0
        for item in self.cart:
            item["subtotal"] = item["quantity"] * item["price"]
            self.cart_tree.insert(
                "",
                "end",
                values=(
                    item["product_name"],
                    f"₹{item['price']:.2f}",
                    item["quantity"],
                    f"₹{item['subtotal']:.2f}"
                )
            )
            total += item["subtotal"]

        self.total_label.config(text=f"Total: ₹{total:.2f}")

    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Selection Required", "Please select a medicine.",
                parent=self.window
            )
            return

        self.cart.pop(self.cart_tree.index(selected[0]))
        self.refresh_cart()

    def save_sale(self):
        customer_id = self.get_selected_customer_id()
        payment_method = self.payment_combo.get()

        if not customer_id:
            messagebox.showwarning(
                "Customer Required", "Please select a customer.",
                parent=self.window
            )
            return

        if not payment_method:
            messagebox.showwarning(
                "Payment Required", "Please select a payment method.",
                parent=self.window
            )
            return

        if not self.cart:
            messagebox.showwarning(
                "Empty Bill", "Please add at least one medicine.",
                parent=self.window
            )
            return

        total = sum(
            float(item["quantity"]) * float(item["price"])
            for item in self.cart
        )

        items_to_save = [
            {
                "product_id": item["product_id"],
                "quantity": int(item["quantity"]),
                "price": float(item["price"]),
                "subtotal": int(item["quantity"]) * float(item["price"])
            }
            for item in self.cart
        ]

        if self.is_editing:
            success, message = self.service.update_sale(
                self.sale_id,
                customer_id,
                total,
                payment_method,
                items_to_save
            )
        else:
            success, message = self.service.create_sale(
                customer_id,
                total,
                payment_method,
                items_to_save
            )

        if success:
            messagebox.showinfo("Success", message, parent=self.window)
            self.window.destroy()
            self.on_saved()
        else:
            messagebox.showerror("Error", message, parent=self.window)