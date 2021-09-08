import tkinter as tk
from tkinter import ttk

class Menubar(ttk.Frame):
    """Builds a menu bar for the top of the main window"""
    def __init__(self, parent, *args, **kwargs):
        ''' Constructor'''
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_menubar()

    def on_exit(self):
        '''Exits program'''
        quit()

    def compile(self):
        '''Solo compila el programa'''
        pass

    def compileRun(self):
        '''Compila y corre el programa'''
        pass

    def init_menubar(self):
        self.menubar = tk.Menu(self.root)
        self.menu_file = tk.Menu(self.menubar) # Creates a "File" menu
        self.menu_file.add_command(label='Exit', command=self.on_exit) # Adds an option to the menu
        self.menubar.add_cascade(menu=self.menu_file, label='File') # Adds File menu to the bar. Can also be used to create submenus.

        self.menu_help = tk.Menu(self.menubar) #Creates a "Run" menu
        self.menu_help.add_command(label='Compilar', command=self.compile)
        self.menu_help.add_command(label='Compilar y ejecutar', command=self.compileRun)
        self.menubar.add_cascade(menu=self.menu_help, label='Run')

        self.root.config(menu=self.menubar)

class GUI(ttk.Frame):
    """Main GUI class"""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def init_gui(self):
        self.root.title('Robotic Hand')
        self.root.geometry("600x400")
        self.root.option_add('*tearOff', 'FALSE') # Disables ability to tear menu bar into own window
        
        # Menu Bar
        self.menubar = Menubar(self.root)

        # Text box frame
        self.textFrame = tk.Frame(self.root)

        # Scroll Bar
        self.scrollbar = ttk.Scrollbar(self.textFrame)
        # packing the scrollbar function
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text Box
        self.text_box = tk.Text(self.textFrame, yscrollcommand=self.scrollbar.set)
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand = 1)
          
        # configuring the scrollbar
        self.scrollbar.config(command=self.text_box.yview)

        self.textFrame.pack(fill=tk.BOTH, expand = 1)

        # Console Frame
        self.consoleFrame = tk.Frame(self.root)

        # Scroll Bar
        self.consoleScrollbar = ttk.Scrollbar(self.consoleFrame)
        self.consoleScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Console List Box
        self.console = tk.Listbox(self.consoleFrame, yscrollcommand=self.consoleScrollbar.set)
        self.console.pack(side=tk.LEFT, fill=tk.X, expand=1)
        
        # configuring the scrollbar
        self.consoleScrollbar.config(command=self.console.yview)

        self.consoleFrame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        # Padding
        for child in self.winfo_children():
            child.configure(padx=10, pady=5)
