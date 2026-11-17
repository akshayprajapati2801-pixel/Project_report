import tkinter as tk
from tkinter import ttk, messagebox

from services.supplier_service import SupplierService


class SupplierForm:

    def __init__(
        self,
        parent,
        on_saved,
        supplier=None
    ):

        self.parent = parent
        self.on_saved = on_saved
        self.supplier = supplier

        self.service = SupplierService()

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Add Supplier"
            if supplier is None
            else "Edit Supplier"
        )

        self.window.geometry("450x450")
        self.window.resizable(False, False)

        self.create_form()

    def create_form(self):

        frame = ttk.Frame(
            self.window,
            padding=25
        )

        frame.pack(
            fill="both",
            expand=True
        )

        title = ttk.Label(
            frame,
            text=(
                "Add Supplier"
                if self.supplier is None
                else "Edit Supplier"
            ),
            font=("Arial", 20, "bold")
        )

        title.pack(
            pady=(0, 20)
        )

        # Supplier Name
        ttk.Label(
            frame,
            text="Supplier Name"
        ).pack(anchor="w")

        self.name_entry = ttk.Entry(
            frame,
            width=45
        )

        self.name_entry.pack(
            pady=(5, 12)
        )

        # Phone
        ttk.Label(
            frame,
            text="Phone"
        ).pack(anchor="w")

        self.phone_entry = ttk.Entry(
            frame,
            width=45
        )

        self.phone_entry.pack(
            pady=(5, 12)
        )

        # Email
        ttk.Label(
            frame,
            text="Email"
        ).pack(anchor="w")

        self.email_entry = ttk.Entry(
            frame,
            width=45
        )

        self.email_entry.pack(
            pady=(5, 12)
        )

        # Address
        ttk.Label(
            frame,
            text="Address"
        ).pack(anchor="w")

        self.address_entry = ttk.Entry(
            frame,
            width=45
        )

        self.address_entry.pack(
            pady=(5, 20)
        )

        # Save button
        save_button = ttk.Button(
            frame,
            text="Save Supplier",
            command=self.save
        )

        save_button.pack(
            pady=10
        )

        # Fill fields when editing
        if self.supplier:

            self.name_entry.insert(
                0,
                self.supplier.get("name", "")
            )

            self.phone_entry.insert(
                0,
                self.supplier.get("phone", "")
            )

            self.email_entry.insert(
                0,
                self.supplier.get("email", "")
            )

            self.address_entry.insert(
                0,
                self.supplier.get("address", "")
            )

    def save(self):

        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()

        if self.supplier:

            success, message = self.service.update(
                self.supplier["id"],
                name,
                phone,
                email,
                address
            )

        else:

            success, message = self.service.create(
                name,
                phone,
                email,
                address
            )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.window.destroy()

            self.on_saved()

        else:

            messagebox.showerror(
                "Error",
                message
            )