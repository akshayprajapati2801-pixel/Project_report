import tkinter as tk
from tkinter import ttk, messagebox

from services.employee_service import EmployeeService
from ui.employees.employee_form import EmployeeForm


class EmployeeList:

    def __init__(self, parent):

        self.parent = parent
        self.service = EmployeeService()

        self.create_ui()
        self.load_employees()

    def create_ui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()

        # ==============================
        # Header
        # ==============================

        header = ttk.Frame(
            self.parent
        )

        header.pack(
            fill="x",
            pady=(0, 20)
        )

        title = ttk.Label(
            header,
            text="Employees",
            font=("Arial", 26, "bold")
        )

        title.pack(
            side="left"
        )

        add_button = ttk.Button(
            header,
            text="+ Add Employee",
            command=self.add_employee
        )

        add_button.pack(
            side="right"
        )

        # ==============================
        # Table
        # ==============================

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
            "department",
            "salary"
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

        # Headings

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "name",
            text="Employee Name"
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
            "department",
            text="Department"
        )

        self.tree.heading(
            "salary",
            text="Salary"
        )

        # Column widths

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
            width=200
        )

        self.tree.column(
            "department",
            width=150
        )

        self.tree.column(
            "salary",
            width=120
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        # ==============================
        # Buttons
        # ==============================

        buttons_frame = ttk.Frame(
            self.parent
        )

        buttons_frame.pack(
            fill="x",
            pady=15
        )

        ttk.Button(
            buttons_frame,
            text="Edit Selected",
            command=self.edit_employee
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_employee
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.load_employees
        ).pack(
            side="left",
            padx=5
        )

    def load_employees(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:

            employees = self.service.get_all()

            for employee in employees:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        employee["id"],
                        employee["name"],
                        employee["phone"] or "",
                        employee["email"] or "",
                        employee["department"] or "",
                        f"{float(employee['salary']):.2f}"
                    )
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def add_employee(self):

        EmployeeForm(
            self.parent.winfo_toplevel(),
            self.load_employees
        )

    def get_selected_employee(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Selection Required",
                "Please select an employee."
            )

            return None

        item = self.tree.item(
            selected[0]
        )

        employee_id = item["values"][0]

        try:

            return self.service.get_by_id(
                employee_id
            )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

            return None

    def edit_employee(self):

        employee = self.get_selected_employee()

        if employee is None:
            return

        EmployeeForm(
            self.parent.winfo_toplevel(),
            self.load_employees,
            employee
        )

    def delete_employee(self):

        employee = self.get_selected_employee()

        if employee is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete employee '{employee['name']}'?"
        )

        if not confirm:
            return

        success, message = self.service.delete(
            employee["id"]
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.load_employees()

        else:

            messagebox.showerror(
                "Error",
                message
            )