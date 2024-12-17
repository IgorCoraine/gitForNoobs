import tkinter as tk
from home import Home

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Git For Noobs")
        self.geometry("1000x1000")
        self.home_screen = Home(self)
        self.home_screen.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
