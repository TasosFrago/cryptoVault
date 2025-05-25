import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class RegisterPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.username_var = tk.StringVar()
        self.cert_file_var = tk.StringVar()

        ttk.Label(self, text="Registration Page", font=('Helvetica', 16)).grid(row=0, column=0, columnspan=3, pady=20, padx=10)

        ttk.Label(self, text="Username:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.username_entry = ttk.Entry(self, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self, text="Certification File:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.cert_file_entry = ttk.Entry(self, textvariable=self.cert_file_var, width=30)
        self.cert_file_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        cert_browse_button = ttk.Button(self, text="Browse", command=self.browse_cert_file)
        cert_browse_button.grid(row=2, column=2, padx=5, pady=5)

        register_btn = ttk.Button(self, text="Register",
                                  command=lambda: controller.attempt_register(self.username_var.get(), self.cert_file_var.get()))
        register_btn.grid(row=3, column=0, columnspan=3, pady=20)

        back_btn = ttk.Button(self, text="Back to Home",
                                command=lambda: controller.show_frame("StartPage"))
        back_btn.grid(row=4, column=0, columnspan=3, pady=10)

        self.columnconfigure(1, weight=1) # Make entry expand

    def browse_cert_file(self):
        filename = filedialog.askopenfilename(title="Select Certification File")
        if filename:
            self.cert_file_var.set(filename)

    def clear_entries(self):
        self.username_var.set("")
        self.cert_file_var.set("")
