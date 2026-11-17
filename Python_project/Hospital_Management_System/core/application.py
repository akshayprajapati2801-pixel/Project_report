
import tkinter as tk

from core.session import Session
from ui.login.login_window import LoginWindow
from ui.dashboard.dashboard import Dashboard


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hospital Management System")
        self.root.geometry("1200x700")
        self.root.minsize(950, 600)
        self.root.resizable(True, True)

        self.login_window = None
        self.dashboard = None

        self.show_login()

    def clear_root(self):
        """Remove the current screen before displaying another."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_root()
        self.dashboard = None

        self.login_window = LoginWindow(
            self.root,
            self.login_success
        )

    def login_success(self):
        self.clear_root()
        self.login_window = None

        self.dashboard = Dashboard(
            self.root,
            self.logout
        )

    def logout(self):
        Session.logout()
        self.show_login()

    def run(self):
        self.root.mainloop()