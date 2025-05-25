import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class StoreFilePage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.file_to_store_var = tk.StringVar()
        self.private_key_var = tk.StringVar()

        ttk.Label(self, text="Store File", font=('Helvetica', 16)).grid(row=0, column=0, columnspan=3, pady=20, padx=10)

        ttk.Label(self, text="File to Store:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.file_to_store_entry = ttk.Entry(self, textvariable=self.file_to_store_var, width=30)
        self.file_to_store_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        store_browse_button = ttk.Button(self, text="Browse", command=self.browse_file_to_store)
        store_browse_button.grid(row=1, column=2, padx=5, pady=5)


        ttk.Label(self, text="Private Key File:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.private_key_entry = ttk.Entry(self, textvariable=self.private_key_var, width=30)
        self.private_key_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        key_browse_button = ttk.Button(self, text="Browse", command=self.browse_private_key)
        key_browse_button.grid(row=2, column=2, padx=5, pady=5)

        store_btn = ttk.Button(self, text="Store File",
                               command=lambda: controller.store_file_action(self.file_to_store_var.get(), self.private_key_var.get()))
        store_btn.grid(row=3, column=0, columnspan=3, pady=20)

        back_btn = ttk.Button(self, text="Back to App Menu",
                                command=lambda: controller.show_frame("AppPage"))
        back_btn.grid(row=4, column=0, columnspan=3, pady=10)

        self.columnconfigure(1, weight=1) # Make entry expand

    def browse_file_to_store(self):
        filename = filedialog.askopenfilename(title="Select File to Store")
        if filename:
            self.file_to_store_var.set(filename)

    def browse_private_key(self):
        filename = filedialog.askopenfilename(title="Select Private Key File")
        if filename:
            self.private_key_var.set(filename)

    def clear_entries(self):
        self.file_to_store_var.set("")
        # Optionally clear private key, or maybe not for convenience
        # self.private_key_var.set("")
