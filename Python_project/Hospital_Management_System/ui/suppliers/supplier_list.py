import tkinter as tk
from tkinter import ttk, messagebox

from services.supplier_service import SupplierService
from ui.suppliers.supplier_form import SupplierForm


class SupplierList:

    def __init__(self, parent):

        self.parent = parent
        self.service = SupplierService()

        self.create_ui()
        self.load_suppliers()

    def create_ui(self):

        for widget in self.parent.winfo_children():
            widget.destroy()

        header = ttk.Frame(
            self.parent
        )

        header.pack(
            fill="x",
            pady=(0, 20)
        )

        title = ttk.Label(
            header,
            text="Suppliers",
            font=("Arial", 26, "bold")
        )

        title.pack(
            side="left"
        )

        add_button = ttk.Button(
            header,
            text="+ Add Supplier",
            command=self.add_supplier
        )

        add_button.pack(
            side="right"
        )

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
            "address"
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

        self.tree.heading(
            "id",
            text="ID"
        )

        self.tree.heading(
            "name",
            text="Supplier Name"
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
            "address",
            text="Address"
        )

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
            "address",
            width=220
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

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
            command=self.edit_supplier
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Delete Selected",
            command=self.delete_supplier
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Refresh",
            command=self.load_suppliers
        ).pack(
            side="left",
            padx=5
        )

    def load_suppliers(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:

            suppliers = self.service.get_all()

            for supplier in suppliers:

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        supplier["id"],
                        supplier["name"],
                        supplier["phone"] or "",
                        supplier["email"] or "",
                        supplier["address"] or ""
                    )
                )

        except Exception as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def add_supplier(self):

        SupplierForm(
            self.parent.winfo_toplevel(),
            self.load_suppliers
        )

    def get_selected_supplier(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "Selection Required",
                "Please select a supplier."
            )

            return None

        item = self.tree.item(
            selected[0]
        )

        supplier_id = item["values"][0]

        return self.service.get_by_id(
            supplier_id
        )

    def edit_supplier(self):

        supplier = self.get_selected_supplier()

        if supplier is None:
            return

        SupplierForm(
            self.parent.winfo_toplevel(),
            self.load_suppliers,
            supplier
        )

    def delete_supplier(self):

        supplier = self.get_selected_supplier()

        if supplier is None:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Delete supplier '{supplier['name']}'?"
        )

        if not confirm:
            return

        success, message = self.service.delete(
            supplier["id"]
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.load_suppliers()

        else:

            messagebox.showerror(
                "Error",
                message
            )