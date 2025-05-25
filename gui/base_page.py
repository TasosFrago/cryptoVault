from tkinter import ttk

from main_frame import MainApp

class BasePage(ttk.Frame):
    def __init__(self, parent, controller: MainApp): # Type hint controller
        ttk.Frame.__init__(self, parent, style="Background.TFrame")
        self.controller = controller
        self.columnconfigure(0, weight=1) # Allows content to center or expand

    def clear_entries(self):
        """Override in subclasses if they have entries to clear upon showing."""
        pass
