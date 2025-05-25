import tkinter as tk
from tkinter import ttk

import gui.base_page

class StartPage(gui.base_page.BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        content_frame = ttk.Frame(self, style="Background.TFrame")
        content_frame.pack(expand=True) # Center content
        label = ttk.Label(content_frame, text="Crypto Vault", style="Header.TLabel")
        label.pack(pady=(60, 30))
        login_button = ttk.Button(content_frame, text="Login", command=lambda: controller.show_frame("LoginPage"))
        login_button.pack(pady=15, ipadx=20, ipady=5, fill=tk.X, padx=50) # Fill X for wider buttons
        register_button = ttk.Button(content_frame, text="Register", command=lambda: controller.show_frame("RegisterPage"))
        register_button.pack(pady=15, ipadx=20, ipady=5, fill=tk.X, padx=50)
