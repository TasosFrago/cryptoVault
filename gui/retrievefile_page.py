import tkinter as tk
from tkinter import ttk, filedialog

import gui.base_page
APP_FONT_FAMILY = "Segoe UI"
APP_FONT_SIZE_NORMAL = 10
APP_FONT_SIZE_LARGE = 12
APP_FONT_SIZE_HEADER = 18
COLOR_PRIMARY = "#007ACC"
COLOR_LIGHT_BG = "#F5F5F5"
COLOR_DARK_FG = "#333333"
COLOR_ENTRY_BG = "#FFFFFF"
COLOR_BUTTON_FG = "#565454"
COLOR_BUTTON_HOVER = "#005999"


class RetrieveFilePage(gui.base_page.BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.user_private_key_var = tk.StringVar()
        self.user_private_key_password_var = tk.StringVar()
        self.selected_file_var = tk.StringVar()

        # Main content frame with padding
        main_content_frame = ttk.Frame(self, style="Background.TFrame", padding=(20, 20))
        main_content_frame.pack(expand=True, fill=tk.BOTH)

        # Title
        ttk.Label(main_content_frame, text="Retrieve Your File", style="SubHeader.TLabel").pack(pady=(0, 15), anchor="w")

        # Frame for Listbox and its label
        listbox_outer_frame = ttk.Frame(main_content_frame, style="Background.TFrame")
        listbox_outer_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(listbox_outer_frame, text="Your Stored Files:").pack(anchor="nw", pady=(0,2))
        
        listbox_inner_frame = ttk.Frame(listbox_outer_frame, style="Background.TFrame") # Frame for listbox and scrollbar
        listbox_inner_frame.pack(fill=tk.BOTH, expand=True)
        listbox_inner_frame.columnconfigure(0, weight=1)
        listbox_inner_frame.rowconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(listbox_inner_frame, height=8, exportselection=False, font=(APP_FONT_FAMILY, APP_FONT_SIZE_NORMAL), bg=COLOR_ENTRY_BG, fg=COLOR_DARK_FG, selectbackground=COLOR_PRIMARY, selectforeground=COLOR_BUTTON_FG, relief="solid", borderwidth=1, activestyle="none")
        self.file_listbox.grid(row=0, column=0, sticky="nsew")
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        scrollbar = ttk.Scrollbar(listbox_inner_frame, orient="vertical", command=self.file_listbox.yview, style="Vertical.TScrollbar")
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.file_listbox.configure(yscrollcommand=scrollbar.set)

        # Frame for input fields (private key, password)
        input_fields_frame = ttk.Frame(main_content_frame, style="Background.TFrame")
        input_fields_frame.pack(fill=tk.X, pady=10)
        input_fields_frame.columnconfigure(1, weight=1) # Allow entry to expand

        ttk.Label(input_fields_frame, text="Your Private Key File:").grid(row=0, column=0, padx=(0,5), pady=5, sticky="w")
        self.private_key_entry = ttk.Entry(input_fields_frame, textvariable=self.user_private_key_var, width=30)
        self.private_key_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        key_browse_button = ttk.Button(input_fields_frame, text="Browse", command=self.browse_private_key, style="Link.TButton")
        key_browse_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        ttk.Label(input_fields_frame, text="Key Password (optional):").grid(row=1, column=0, padx=(0,5), pady=5, sticky="w")
        self.private_key_password_entry = ttk.Entry(input_fields_frame, textvariable=self.user_private_key_password_var, width=30, show="*")
        self.private_key_password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew", columnspan=2)

        # Frame for action buttons
        action_buttons_frame = ttk.Frame(main_content_frame, style="Background.TFrame")
        action_buttons_frame.pack(fill=tk.X, pady=(10,0))
        
        retrieve_btn = ttk.Button(action_buttons_frame, text="Retrieve and Decrypt", command=self.retrieve_selected_file_action)
        retrieve_btn.pack(side=tk.LEFT, padx=(0,10), ipady=4, ipadx=10) #anchor="center"
        back_btn = ttk.Button(action_buttons_frame, text="Back to Menu", style="Link.TButton", command=lambda: controller.show_frame("AppPage"))
        back_btn.pack(side=tk.LEFT) #anchor="center"


    def browse_private_key(self):
        filename = filedialog.askopenfilename(title="Select Your Private Key File", parent=self, filetypes=[("Key files", "*.key *.pem"), ("All files", "*.*")])
        if filename: self.user_private_key_var.set(filename)

    def on_file_select(self, event):
        widget = event.widget
        try:
            if widget.curselection(): # Check if there is a selection
                selected_index = widget.curselection()[0]
                selected_file = widget.get(selected_index).strip() # Strip spaces from listbox item
                self.selected_file_var.set(selected_file)
            else:
                self.selected_file_var.set("")
        except IndexError: self.selected_file_var.set("")

    def retrieve_selected_file_action(self):
        selected = self.selected_file_var.get()
        pk_path = self.user_private_key_var.get()
        pk_pass = self.user_private_key_password_var.get()
        self.controller.retrieve_file_action(selected, pk_path, pk_pass)

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        if self.controller.current_user and self.controller.current_user.vault_folder:
            try:
                user_files = self.controller.vault.list_user_files(self.controller.current_user.vault_folder)
                if not user_files:
                    self.file_listbox.insert(tk.END, " No files stored yet. ")
                else:
                    for f_name in user_files: self.file_listbox.insert(tk.END, f" {f_name} ") # Add padding
            except Exception as e:
                self.file_listbox.insert(tk.END, " Error listing files. ")
                print(f"Error refreshing file list: {e}")
        else:
            self.file_listbox.insert(tk.END, " Not logged in. ")
        self.selected_file_var.set("")
    
    def clear_entries(self):
        # self.user_private_key_var.set("") # Often users want to keep this for multiple retrievals
        # self.user_private_key_password_var.set("")
        self.selected_file_var.set("")
        if self.file_listbox.size() > 0:
            self.file_listbox.selection_clear(0, tk.END)
        if hasattr(self, 'private_key_entry') and self.controller.current_user: # Only focus if logged in
            self.private_key_entry.focus_set()
