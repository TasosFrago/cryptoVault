from tkinter import ttk

class AppPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Label(self, text="Main Application", font=('Helvetica', 16)).pack(pady=20)

        store_button = ttk.Button(self, text="Store File", command=lambda: controller.show_frame("StoreFilePage"))
        store_button.pack(pady=10, ipadx=10)

        retrieve_button = ttk.Button(self, text="Retrieve File", command=lambda: controller.show_frame("RetrieveFilePage"))
        retrieve_button.pack(pady=10, ipadx=10)

        logout_button = ttk.Button(self, text="Logout", command=lambda: controller.show_frame("StartPage"))
        logout_button.pack(pady=30, ipadx=10)
