# ==========================================
# Login Window
# ==========================================

import tkinter as tk
from tkinter import ttk, messagebox

from services.auth_service import AuthService


class LoginWindow:

    def __init__(self, root, on_login_success):

        self.root = root
        self.on_login_success = on_login_success

        self.auth_service = AuthService()

        self.root.title(
            "Hospital Management System - Login"
        )

        self.root.geometry(
            "500x400"
        )

        self.root.resizable(
            False,
            False
        )

        self.create_widgets()

    # --------------------------------------
    # Create Login UI
    # --------------------------------------

    def create_widgets(self):

        main_frame = ttk.Frame(
            self.root,
            padding=30
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ----------------------------------
        # Title
        # ----------------------------------

        title_label = ttk.Label(
            main_frame,
            text="Hospital Management System",
            font=("Arial", 20, "bold")
        )

        title_label.pack(
            pady=(20, 10)
        )

        subtitle_label = ttk.Label(
            main_frame,
            text="Login to your account",
            font=("Arial", 11)
        )

        subtitle_label.pack(
            pady=(0, 25)
        )

        # ----------------------------------
        # Username
        # ----------------------------------

        username_label = ttk.Label(
            main_frame,
            text="Username"
        )

        username_label.pack(
            anchor="w"
        )

        self.username_entry = ttk.Entry(
            main_frame,
            width=40
        )

        self.username_entry.pack(
            pady=(5, 15)
        )

        # ----------------------------------
        # Password
        # ----------------------------------

        password_label = ttk.Label(
            main_frame,
            text="Password"
        )

        password_label.pack(
            anchor="w"
        )

        self.password_entry = ttk.Entry(
            main_frame,
            width=40,
            show="*"
        )

        self.password_entry.pack(
            pady=(5, 20)
        )

        # ----------------------------------
        # Login Button
        # ----------------------------------

        login_button = ttk.Button(
            main_frame,
            text="Login",
            command=self.login
        )

        login_button.pack(
            pady=10
        )

        # ----------------------------------
        # Status
        # ----------------------------------

        self.status_label = ttk.Label(
            main_frame,
            text=""
        )

        self.status_label.pack(
            pady=10
        )

        # ----------------------------------
        # Enter Key
        # ----------------------------------

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.username_entry.focus()

    # --------------------------------------
    # Login
    # --------------------------------------

    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        success, message = self.auth_service.login(
            username,
            password
        )

        if success:

            self.status_label.config(
                text=message
            )

            self.on_login_success()

        else:

            self.status_label.config(
                text=message
            )

            messagebox.showerror(
                "Login Failed",
                message
            )