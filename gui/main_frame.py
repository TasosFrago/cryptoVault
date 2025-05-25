import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from login_page import LoginPage
from registration_page import RegisterPage
from retrievefile_page import RetrieveFilePage
from start_page import StartPage
from storefile_page import StoreFilePage
from app_page import AppPage


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("CryptoVault")
        self.geometry("500x400")

        # Container for all frames
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_user_files = [] # To store dummy file names for retrieval page

        for F in (StartPage, LoginPage, RegisterPage, AppPage, StoreFilePage, RetrieveFilePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        # If navigating to retrieve page, refresh its list (if needed)
        if page_name == "RetrieveFilePage":
            self.frames[page_name].refresh_file_list()
        # If navigating to login page (e.g., after registration), clear previous entries
        if page_name == "LoginPage":
            self.frames[page_name].clear_entries()
        if page_name == "RegisterPage":
            self.frames[page_name].clear_entries()


    def get_frame(self, page_name):
        return self.frames[page_name]

    # --- Placeholder backend interactions ---
    def attempt_login(self, username, cert_file_path):
        print(f"Attempting login for user: {username}, cert: {cert_file_path}")
        if username and cert_file_path: # Dummy check
            messagebox.showinfo("Login Info", "Login button pressed.\n(Backend logic needed here)")
            self.show_frame("AppPage")
        else:
            messagebox.showerror("Login Error", "Username and Certification File are required.")

    def attempt_register(self, username, cert_file_path):
        print(f"Attempting registration for user: {username}, cert: {cert_file_path}")
        if username and cert_file_path: # Dummy check
            messagebox.showinfo("Registration Info", "Register button pressed.\n(Backend logic needed here)\nRedirecting to Login.")
            self.show_frame("LoginPage")
        else:
            messagebox.showerror("Registration Error", "Username and Certification File are required.")


    def store_file_action(self, file_to_store_path, private_key_path):
        print(f"Storing file: {file_to_store_path} using key: {private_key_path}")
        # Replace with your actual file storing logic
        if file_to_store_path and private_key_path: # Dummy check
            # Add the filename (not path) to our dummy list for retrieval
            file_name = file_to_store_path.split('/')[-1]
            if file_name not in self.current_user_files:
                self.current_user_files.append(file_name)
            messagebox.showinfo("Store File Info", f"Store button pressed for {file_name}.\n(Backend logic needed here)")
            self.frames["StoreFilePage"].clear_entries() # Clear entries after storing
        else:
            messagebox.showerror("Store File Error", "File to store and Private Key are required.")


    def retrieve_file_action(self, selected_file, private_key_path):
        print(f"Retrieving file: {selected_file} using key: {private_key_path}")
        # Replace with your actual file retrieval logic (e.g., open folder)
        if selected_file and private_key_path: # Dummy check
            messagebox.showinfo("Retrieve File Info", f"Retrieving {selected_file}.\n(Backend logic to open folder needed here)")
            # Example: self.open_file_location(retrieved_file_path)
        elif not selected_file:
            messagebox.showerror("Retrieve File Error", "Please select a file from the list.")
        else:
            messagebox.showerror("Retrieve File Error", "Private Key is required.")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
