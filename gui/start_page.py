from tkinter import ttk

class StartPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 12))
        style.configure("Header.TLabel", font=('Helvetica', 18, 'bold'))

        label = ttk.Label(self, text="Welcome to File Guardian", style="Header.TLabel")
        label.pack(pady=40)

        login_button = ttk.Button(self, text="Login", command=lambda: controller.show_frame("LoginPage"))
        login_button.pack(pady=10, ipadx=10)

        register_button = ttk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterPage"))
        register_button.pack(pady=10, ipadx=10)
