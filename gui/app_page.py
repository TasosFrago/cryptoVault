import tkinter as tk
from tkinter import ttk

import gui.base_page


class AppPage(gui.base_page.BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        content_frame = ttk.Frame(self, style="Background.TFrame")
        content_frame.pack(expand=True)
        ttk.Label(content_frame, text="Main Menu", style="Header.TLabel").pack(pady=(40,30))
        store_button = ttk.Button(content_frame, text="Store File", command=lambda: controller.show_frame("StoreFilePage"))
        store_button.pack(pady=15, ipadx=30, ipady=5, fill=tk.X, padx=100)
        retrieve_button = ttk.Button(content_frame, text="Retrieve File", command=lambda: controller.show_frame("RetrieveFilePage"))
        retrieve_button.pack(pady=15, ipadx=30, ipady=5, fill=tk.X, padx=100)
        logout_button = ttk.Button(content_frame, text="Logout", style="Link.TButton", command=lambda: controller.show_frame("StartPage", clear_user_on_start=True))
        logout_button.pack(pady=(40,15), ipadx=10)
