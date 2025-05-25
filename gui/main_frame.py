import shutil
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import os
import platform
import subprocess

from gui.starting_page import StartPage
from gui.login_page import LoginPage
from gui.retrievefile_page import RetrieveFilePage
from gui.registration_page import RegisterPage
from gui.storefile_page import StoreFilePage
from gui.app_page import AppPage

from crypto.user_actions import User, TEMP_DIR
from crypto.vault_logic import BASE_STORAGE_PATH, Vault

# --- Global Style Configuration (same as before) ---
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


class MainApp(ThemedTk):
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs)
        self.set_theme("arc")
        self.title("Crypto Vault")
        self.geometry("700x600")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.current_user: User | None = None
        try:
            self.vault = Vault()
        except Exception as e:
            messagebox.showerror("Vault Initialization Error", f"Critical error: Could not initialize the Vault.\n{e}\nApplication will exit.")
            self.destroy()
            return

        self.style = ttk.Style(self)
        self.configure_styles()

        container = ttk.Frame(self, style="Background.TFrame")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, LoginPage, RegisterPage, AppPage, StoreFilePage, RetrieveFilePage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        if hasattr(self, 'vault'): # Ensure vault was initialized
            self.show_frame("StartPage")

    def configure_styles(self):
        self.style.configure("Background.TFrame", background=COLOR_LIGHT_BG)
        self.style.configure(".", font=(APP_FONT_FAMILY, APP_FONT_SIZE_NORMAL), padding=5)
        self.style.configure("TLabel", background=COLOR_LIGHT_BG, foreground=COLOR_DARK_FG, padding=(5, 5, 5, 10))
        self.style.configure("Header.TLabel", font=(APP_FONT_FAMILY, APP_FONT_SIZE_HEADER, 'bold'), background=COLOR_LIGHT_BG, foreground=COLOR_PRIMARY)
        self.style.configure("SubHeader.TLabel", font=(APP_FONT_FAMILY, APP_FONT_SIZE_LARGE, 'bold'), background=COLOR_LIGHT_BG, foreground=COLOR_DARK_FG)
        self.style.configure("TButton", font=(APP_FONT_FAMILY, APP_FONT_SIZE_LARGE), padding=(10, 8), relief="flat", background=COLOR_PRIMARY, foreground=COLOR_BUTTON_FG)
        self.style.map("TButton", background=[('active', COLOR_BUTTON_HOVER), ('pressed', COLOR_BUTTON_HOVER)], relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
        self.style.configure("Link.TButton", font=(APP_FONT_FAMILY, APP_FONT_SIZE_NORMAL),padding=(5,5), foreground=COLOR_PRIMARY, background=COLOR_LIGHT_BG) # For "Back" or less prominent buttons
        self.style.map("Link.TButton", foreground=[('active', COLOR_BUTTON_HOVER)], background=[('active', COLOR_LIGHT_BG)])
        self.style.configure("TEntry", font=(APP_FONT_FAMILY, APP_FONT_SIZE_NORMAL), padding=8, relief="flat", fieldbackground=COLOR_ENTRY_BG)
        self.style.configure("TListbox", font=(APP_FONT_FAMILY, APP_FONT_SIZE_NORMAL), padding=5, relief="solid", background=COLOR_ENTRY_BG, borderwidth=1)
        self.style.map("TListbox", background=[('focus', COLOR_ENTRY_BG)], selectbackground=[('focus', COLOR_PRIMARY)], selectforeground=[('focus', COLOR_BUTTON_FG)])
        self.configure(background=COLOR_LIGHT_BG) # Root window background

    def show_frame(self, page_name: str, clear_user_on_start: bool = False):
        if clear_user_on_start and page_name == "StartPage":
            self.current_user = None
            print("User logged out.")
        frame = self.frames[page_name]
        frame.tkraise()
        if self.current_user and page_name == "RetrieveFilePage":
            # Ensure the frame instance has the method before calling
            retrieve_page_frame = self.frames.get("RetrieveFilePage")
            if retrieve_page_frame and hasattr(retrieve_page_frame, 'refresh_file_list'):
                retrieve_page_frame.refresh_file_list() # type: ignore

        current_page_frame = self.frames.get(page_name)
        if current_page_frame and hasattr(current_page_frame, 'clear_entries'):
            current_page_frame.clear_entries() # type: ignore

    def get_frame(self, page_name: str) -> ttk.Frame:
        return self.frames[page_name]

    def attempt_login(self, username: str, cert_file_path: str):
        if not username or not cert_file_path:
            messagebox.showerror("Login Error", "Username and Certification File are required.", parent=self.get_frame("LoginPage"))
            return
        try:
            self.current_user = User(username, cert_file_path)
            usr_dir = os.path.join(BASE_STORAGE_PATH, self.current_user.vault_folder)
            if not os.path.exists(usr_dir):
                raise Exception(f"User: {username} not registered.")
            messagebox.showinfo("Login Success", f"Welcome, {self.current_user.username_alias}!\nUser ID (from cert): {self.current_user.user_id}", parent=self.get_frame("LoginPage"))
            self.show_frame("AppPage")
        except Exception as e:
            self.current_user = None
            messagebox.showerror("Login Failed", f"Could not log in: {e}", parent=self.get_frame("LoginPage"))
            # self.show_frame("StartPage", clear_user_on_start=True)

    def attempt_register(self, username: str, cert_file_path: str):
        if not username or not cert_file_path:
            messagebox.showerror("Registration Error", "Username and Certification File are required.", parent=self.get_frame("RegisterPage"))
            return
        try:
            _ = User(username, cert_file_path)

            print("Registering New user")
            self.vault.register_user(username, cert_file_path)
            messagebox.showinfo("Register Success", f"User {username} created", parent=self.get_frame("RegisterPage"))
            self.show_frame("LoginPage")
        except Exception as e:
            messagebox.showerror("Registration Failed", f"Could not complete registration: {e}", parent=self.get_frame("RegisterPage"))

    def store_file_action(self, file_to_store_path: str):
        if not self.current_user:
            messagebox.showerror("Error", "No user logged in.", parent=self.get_frame("StoreFilePage"))
            return
        if not file_to_store_path:
            messagebox.showerror("Store File Error", "File to store is required.", parent=self.get_frame("StoreFilePage"))
            return
        try:
            success = self.current_user.store_file(self.vault, file_to_store_path)
            if success:
                messagebox.showinfo("Store File Success", f"File '{os.path.basename(file_to_store_path)}' stored successfully.", parent=self.get_frame("StoreFilePage"))
                # Refresh file list on retrieve page if it exists
                retrieve_page_frame = self.frames.get("RetrieveFilePage")
                if retrieve_page_frame and hasattr(retrieve_page_frame, 'refresh_file_list'):
                    retrieve_page_frame.refresh_file_list() # type: ignore
            else:
                messagebox.showerror("Store File Failed", "Vault could not store the file. Check console for details.", parent=self.get_frame("StoreFilePage"))
        except Exception as e:
            messagebox.showerror("Store File Error", f"An error occurred: {e}", parent=self.get_frame("StoreFilePage"))

    def retrieve_file_action(self, selected_file: str, user_private_key_path: str, user_private_key_password: str | None):
        if not self.current_user:
            messagebox.showerror("Error", "No user logged in.", parent=self.get_frame("RetrieveFilePage"))
            return
        if not selected_file:
            messagebox.showerror("Retrieve File Error", "Please select a file from the list.", parent=self.get_frame("RetrieveFilePage"))
            return
        if not user_private_key_path:
            messagebox.showerror("Retrieve File Error", "User's Private Key path is required.", parent=self.get_frame("RetrieveFilePage"))
            return

        pk_password = user_private_key_password if user_private_key_password else None

        try:
            result_path_or_status = self.current_user.retrieve_decrypt_file(
                self.vault, selected_file, user_private_key_path, pk_password
            )

            if result_path_or_status:
                messagebox.showinfo("Retrieve Success", f"File '{selected_file}' decrypted and saved to:\n{result_path_or_status}\nOpening TEMP folder.", parent=self.get_frame("RetrieveFilePage"))
                self.open_user_temp_folder()
            else:
                messagebox.showerror("Retrieve Failed", f"Could not retrieve or decrypt '{selected_file}'. Wrong key", parent=self.get_frame("RetrieveFilePage"))
        except Exception as e:
            messagebox.showerror("Retrieve Error", f"An unexpected error occurred: {e}", parent=self.get_frame("RetrieveFilePage"))

    def open_user_temp_folder(self):
        """Opens the app_utils.TEMP_DIR_USER in the system's file explorer."""
        path_to_open = TEMP_DIR
        try:
            if platform.system() == "Windows":
                os.startfile(path_to_open) # type: ignore
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", path_to_open], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.Popen(["xdg-open", path_to_open], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            messagebox.showwarning("Open Folder", f"Could not automatically open the folder: {path_to_open}\nError: {e}", parent=self)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?", parent=self):

            # Clean tmp for safety
            for file in os.listdir(TEMP_DIR):
                file_path = os.path.join(TEMP_DIR, file)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

            self.destroy()
