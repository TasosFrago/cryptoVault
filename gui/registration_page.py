import tkinter as tk
from tkinter import ttk, filedialog

import gui.base_page

class RegisterPage(gui.base_page.BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.username_var = tk.StringVar()
        self.cert_file_var = tk.StringVar()

        content_frame = ttk.Frame(self, style="Background.TFrame", padding=(30,30))
        content_frame.pack(expand=True, fill=tk.BOTH) # Fill for responsiveness

        form_area = ttk.Frame(content_frame, style="Background.TFrame") # Inner frame for form elements
        form_area.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # Center the form area

        ttk.Label(form_area, text="Create Account", style="SubHeader.TLabel").grid(row=0, column=0, columnspan=3, pady=(0, 25), sticky="w")
        ttk.Label(form_area, text="Username Alias:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.username_entry = ttk.Entry(form_area, textvariable=self.username_var, width=35)
        self.username_entry.grid(row=1, column=1, padx=5, pady=8, sticky="ew", columnspan=2)
        ttk.Label(form_area, text="Certificate File:").grid(row=2, column=0, padx=5, pady=8, sticky="w")
        self.cert_file_entry = ttk.Entry(form_area, textvariable=self.cert_file_var, width=25)
        self.cert_file_entry.grid(row=2, column=1, padx=5, pady=8, sticky="ew")
        cert_browse_button = ttk.Button(form_area, text="Browse", command=self.browse_cert_file, style="Link.TButton")
        cert_browse_button.grid(row=2, column=2, padx=(0,5), pady=8, sticky="e")
        
        button_frame = ttk.Frame(form_area, style="Background.TFrame") # Frame for buttons
        button_frame.grid(row=3, column=0, columnspan=3, pady=(30,0))

        register_btn = ttk.Button(button_frame, text="Register", command=lambda: controller.attempt_register(self.username_var.get(), self.cert_file_var.get()))
        register_btn.pack(side=tk.LEFT, padx=5, ipady=4, ipadx=10)
        back_btn = ttk.Button(button_frame, text="Back", style="Link.TButton", command=lambda: controller.show_frame("StartPage"))
        back_btn.pack(side=tk.LEFT, padx=5)
        
        form_area.columnconfigure(1, weight=1) # Make entry expand

    def browse_cert_file(self):
        filename = filedialog.askopenfilename(title="Select Your Certificate File", parent=self, filetypes=[("Certificate files", "*.crt *.pem"), ("All files", "*.*")])
        if filename: self.cert_file_var.set(filename)
    
    def clear_entries(self):
        self.username_var.set("")
        self.cert_file_var.set("")
        if hasattr(self, 'username_entry'): self.username_entry.focus_set()
