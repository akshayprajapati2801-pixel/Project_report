import tkinter as tk
from tkinter import ttk, messagebox

from services.employee_service import EmployeeService


class EmployeeForm:

    def __init__(
        self,
        parent,
        on_saved,
        employee=None
    ):

        self.parent = parent
        self.on_saved = on_saved
        self.employee = employee

        self.service = EmployeeService()

        self.window = tk.Toplevel(parent)

        self.window.title(
            "Add Employee"
            if employee is None
            else "Edit Employee"
        )

        self.window.geometry("450x550")
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
                "Add Employee"
                if self.employee is None
                else "Edit Employee"
            ),
            font=("Arial", 20, "bold")
        )

        title.pack(
            pady=(0, 20)
        )

        # Employee Name
        ttk.Label(
            frame,
            text="Employee Name"
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

        # Department
        ttk.Label(
            frame,
            text="Department"
        ).pack(anchor="w")

        self.department_combo = ttk.Combobox(
            frame,
            values=[
                "Administration",
                "Nursing",
                "Pharmacy",
                "Laboratory",
                "Reception",
                "Accounts",
                "Human Resources",
                "Maintenance",
                "Other"
            ],
            state="readonly",
            width=42
        )

        self.department_combo.pack(
            pady=(5, 12)
        )

        # Salary
        ttk.Label(
            frame,
            text="Salary"
        ).pack(anchor="w")

        self.salary_entry = ttk.Entry(
            frame,
            width=45
        )

        self.salary_entry.pack(
            pady=(5, 20)
        )

        # Save button
        save_button = ttk.Button(
            frame,
            text="Save Employee",
            command=self.save
        )

        save_button.pack(
            pady=10
        )

        # Fill fields when editing
        if self.employee:

            self.name_entry.insert(
                0,
                self.employee.get("name", "")
            )

            self.phone_entry.insert(
                0,
                self.employee.get("phone", "")
            )

            self.email_entry.insert(
                0,
                self.employee.get("email", "")
            )

            department = self.employee.get(
                "department",
                ""
            )

            if department:
                self.department_combo.set(
                    department
                )

            self.salary_entry.insert(
                0,
                str(
                    self.employee.get(
                        "salary",
                        ""
                    )
                )
            )

    def save(self):

        name = self.name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        department = self.department_combo.get()
        salary = self.salary_entry.get()

        if self.employee:

            success, message = self.service.update(
                self.employee["id"],
                name,
                phone,
                email,
                department,
                salary
            )

        else:

            success, message = self.service.create(
                name,
                phone,
                email,
                department,
                salary
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