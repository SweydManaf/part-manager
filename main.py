from tkinter import *
from tkinter import ttk
from window import MainWindow

class MainApp:
    def __init__(self):
        self.root = Tk()
        self.root.title('Part Manager')

        # SET THE WINDOWS CONFIGURATION
        self.width = 640
        self.height = 500
        self.sys_width = int((self.root.winfo_screenwidth() / 2) - (self.width/2))
        self.sys_height = int((self.root.winfo_screenheight() / 2) - (self.height/2))

        self.root.geometry(f'{self.width}x{self.height}+{self.sys_width}+{self.sys_height}')
        self.root.resizable(width=False, height=False)


        # SET THE THEME
        self.root.tk.call('source', 'azure.tcl')
        self.root.tk.call('set_theme', 'light')

        # START THE APP
        MainWindow(self.root)
        self.root.mainloop()

if __name__ == '__main__':
    MainApp()