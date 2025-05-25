import tkinter as tk
from tkinter import ttk, filedialog

import gui.base_page

class StoreFilePage(gui.base_page.BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.file_to_store_var = tk.StringVar()

        content_frame = ttk.Frame(self, style="Background.TFrame", padding=(30,30))
        content_frame.pack(expand=True, fill=tk.BOTH)

        form_area = ttk.Frame(content_frame, style="Background.TFrame")
        form_area.place(relx=0.5, rely=0.4, anchor=tk.CENTER) # Adjust rely for better centering

        ttk.Label(form_area, text="Store a New File", style="SubHeader.TLabel").grid(row=0, column=0, columnspan=3, pady=(0,25), sticky="w")
        ttk.Label(form_area, text="File to Store:").grid(row=1, column=0, padx=5, pady=8, sticky="w")
        self.file_to_store_entry = ttk.Entry(form_area, textvariable=self.file_to_store_var, width=30)
        self.file_to_store_entry.grid(row=1, column=1, padx=5, pady=8, sticky="ew")
        store_browse_button = ttk.Button(form_area, text="Browse", command=self.browse_file_to_store, style="Link.TButton")
        store_browse_button.grid(row=1, column=2, padx=(0,5), pady=8, sticky="e")

        button_frame = ttk.Frame(form_area, style="Background.TFrame")
        button_frame.grid(row=2, column=0, columnspan=3, pady=(30,0)) # Adjusted row from 3 to 2

        store_btn = ttk.Button(button_frame, text="Store Securely", command=lambda: controller.store_file_action(self.file_to_store_var.get()))
        store_btn.pack(side=tk.LEFT, padx=5, ipady=4, ipadx=10)
        back_btn = ttk.Button(button_frame, text="Back to Menu", style="Link.TButton", command=lambda: controller.show_frame("AppPage"))
        back_btn.pack(side=tk.LEFT, padx=5)

        form_area.columnconfigure(1, weight=1)

    def browse_file_to_store(self):
        filename = filedialog.askopenfilename(title="Select File to Store", parent=self)
        if filename: self.file_to_store_var.set(filename)
    
    def clear_entries(self):
        self.file_to_store_var.set("")
        if hasattr(self, 'file_to_store_entry'): self.file_to_store_entry.focus_set()
