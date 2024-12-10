import tkinter as tk
from home import Home

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Git GUI App")
        self.geometry("800x600")
        self.home_screen = Home(self)
        self.home_screen.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
