# ==========================================
# Patient Form
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox

from services.customer_service import CustomerService


class CustomerForm:

    def __init__(
        self,
        parent,
        on_saved,
        customer=None
    ):

        self.parent = parent
        self.on_saved = on_saved
        self.customer = customer

        self.service = CustomerService()

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Add Patient"
            if customer is None
            else "Edit Patient"
        )

        self.window.geometry("450x550")
        self.window.resizable(False, False)

        self.create_form()

    # --------------------------------------
    # Create Form
    # --------------------------------------

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
                "Add Patient"
                if self.customer is None
                else "Edit Patient"
            ),
            font=("Arial", 20, "bold")
        )

        title.pack(
            pady=(0, 20)
        )

        # ----------------------------------
        # Name
        # ----------------------------------

        ttk.Label(
            frame,
            text="Patient Name"
        ).pack(anchor="w")

        self.name_entry = ttk.Entry(
            frame,
            width=45
        )

        self.name_entry.pack(
            pady=(5, 12)
        )

        # ----------------------------------
        # Phone
        # ----------------------------------

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

        # ----------------------------------
        # Email
        # ----------------------------------

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

        # ----------------------------------
        # Address
        # ----------------------------------

        ttk.Label(
            frame,
            text="Address"
        ).pack(anchor="w")

        self.address_entry = ttk.Entry(
            frame,
            width=45
        )

        self.address_entry.pack(
            pady=(5, 12)
        )

        # ----------------------------------
        # Age
        # ----------------------------------

        ttk.Label(
            frame,
            text="Age"
        ).pack(anchor="w")

        self.age_entry = ttk.Entry(
            frame,
            width=45
        )

        self.age_entry.pack(
            pady=(5, 12)
        )

        # ----------------------------------
        # Gender
        # ----------------------------------

        ttk.Label(
            frame,
            text="Gender"
        ).pack(anchor="w")

        self.gender_combo = ttk.Combobox(
            frame,
            values=[
                "Male",
                "Female",
                "Other"
            ],
            state="readonly",
            width=42
        )

        self.gender_combo.pack(
            pady=(5, 20)
        )

        # ----------------------------------
        # Save Button
        # ----------------------------------

        save_button = ttk.Button(
            frame,
            text="Save Patient",
            command=self.save
        )

        save_button.pack(
            pady=10
        )

        # ----------------------------------
        # Load Existing Patient
        # ----------------------------------

        if self.customer:

            self.name_entry.insert(
                0,
                self.customer.get("name", "")
            )

            self.phone_entry.insert(
                0,
                self.customer.get("phone", "")
            )

            self.email_entry.insert(
                0,
                self.customer.get("email", "")
            )

            self.address_entry.insert(
                0,
                self.customer.get("address", "")
            )

            if self.customer.get("age") is not None:

                self.age_entry.insert(
                    0,
                    str(self.customer["age"])
                )

            gender = self.customer.get(
                "gender",
                ""
            )

            if gender:

                self.gender_combo.set(
                    gender
                )

    # --------------------------------------
    # Save Patient
    # --------------------------------------

    def save(self):

        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        age = self.age_entry.get()
        gender = self.gender_combo.get()

        if self.customer:

            success, message = self.service.update(
                self.customer["id"],
                name,
                phone,
                email,
                address,
                age,
                gender
            )

        else:

            success, message = self.service.create(
                name,
                phone,
                email,
                address,
                age,
                gender
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