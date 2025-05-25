import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class RetrieveFilePage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.private_key_var = tk.StringVar()
        self.selected_file_var = tk.StringVar()

        ttk.Label(self, text="Retrieve File", font=('Helvetica', 16)).grid(row=0, column=0, columnspan=3, pady=10, padx=10)

        ttk.Label(self, text="Your Stored Files:").grid(row=1, column=0, padx=10, pady=5, sticky="nw")
        
        self.file_listbox = tk.Listbox(self, height=6, exportselection=False) # exportselection=False allows programmatic selection to persist
        self.file_listbox.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)

        # Scrollbar for listbox
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.file_listbox.yview)
        scrollbar.grid(row=1, column=2, padx=(0,10), pady=5, sticky="ns")
        self.file_listbox.configure(yscrollcommand=scrollbar.set)


        ttk.Label(self, text="Private Key File:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.private_key_entry = ttk.Entry(self, textvariable=self.private_key_var, width=30)
        self.private_key_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        key_browse_button = ttk.Button(self, text="Browse", command=self.browse_private_key)
        key_browse_button.grid(row=2, column=2, padx=5, pady=10)


        retrieve_btn = ttk.Button(self, text="Open File Location",
                                  command=self.retrieve_selected_file)
        retrieve_btn.grid(row=3, column=0, columnspan=3, pady=10)

        back_btn = ttk.Button(self, text="Back to App Menu",
                                command=lambda: controller.show_frame("AppPage"))
        back_btn.grid(row=4, column=0, columnspan=3, pady=10)

        self.columnconfigure(1, weight=1) # Make listbox and entry expand

    def browse_private_key(self):
        filename = filedialog.askopenfilename(title="Select Private Key File")
        if filename:
            self.private_key_var.set(filename)

    def on_file_select(self, event):
        # Get selected line index
        try:
            selected_index = self.file_listbox.curselection()[0]
            selected_file = self.file_listbox.get(selected_index)
            self.selected_file_var.set(selected_file)
            print(f"Selected file from list: {selected_file}")
        except IndexError:
            self.selected_file_var.set("") # No item selected

    def retrieve_selected_file(self):
        selected_file = self.selected_file_var.get()
        private_key = self.private_key_var.get()
        self.controller.retrieve_file_action(selected_file, private_key)

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END) # Clear existing items
        # Populate with dummy data or files from controller
        # For demonstration, using files from controller.current_user_files
        if not self.controller.current_user_files:
            self.file_listbox.insert(tk.END, "No files stored yet.")
        else:
            for f_name in self.controller.current_user_files:
                self.file_listbox.insert(tk.END, f_name)
        self.selected_file_var.set("") # Clear selection
