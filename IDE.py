import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import compiler

class Menubar(ttk.Frame):
    """Builds a menu bar for the top of the main window"""
    def __init__(self, parent, GUI, *args, **kwargs):
        ''' Constructor'''
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.GUI = GUI
        self.file_name = None
        self.init_menubar()

    def on_exit(self):
        quit()

    def load_file(self):
        file = filedialog.askopenfile(initialdir = ".",
                                          title = "Select a File",
                                          filetypes = (("Text files", "*.txt*"),
                                                       ("all files", "*")))
        self.GUI.text_box.delete('1.0', tk.END)
        self.GUI.text_box.insert('1.0', file.read())
        self.file_name = file.name
        file.close()

    def save_file_as(self):
        file = filedialog.asksaveasfile(initialdir = ".",
                                          title = "Select a File",
                                          filetypes = (("Text files", "*.txt*"),
                                                       ("all files", "*")))
        if(file):
            file.write( self.GUI.text_box.get('1.0', "end-1c") ) #end-1c means end minus last character, so it excludes the newline at the end
            self.file_name = file.name
            file.close()
            return True

    def save_file(self):
        if(self.file_name):
            with open(self.file_name, 'w') as file:
                file.write( self.GUI.text_box.get('1.0', "end-1c") )
                return True
        else:
            if(self.save_file_as()): return True
        return False

    def compile(self):
        '''Solo compila el programa'''
        self.GUI.cls()
        # First it saves the file
        if(not self.save_file()):
            print("No se pudo guardar el archivo, por lo tanto no se compiló")
            return False
        # Then it obtains the text from the saved file
        with open(self.file_name, 'r') as file:
            codeString = file.read()
        # Then do stuff with the string
        compiler.clearAll()
        compiler.compile(codeString, self.GUI)
        return True

    def compileRun(self):
        '''Compila y corre el programa'''
        # Primero compila el programa
        if(not self.compile()):
            print("No se guardó el archivo")
            return

        # Luego lo corre
        compiler.run_main()
        compiler.clearAll()

    # Manejo de estado para ctrl+s
    def root_key_pressed(self, event):
        if event.state == 0x4 and event.keycode == 39: # ctrl + s
            self.save_file()

    def init_menubar(self):
        self.menubar = tk.Menu(self.root)
        self.menu_file = tk.Menu(self.menubar) # Creates a "File" menu
        self.menu_file.add_command(label='Cargar Archivo', command=self.load_file) # Adds an option to the menu
        self.menu_file.add_command(label='Guardar Archivo', command=self.save_file) # Adds an option to the menu
        self.menu_file.add_command(label='Guardar Archivo Como...', command=self.save_file_as) # Adds an option to the menu
        self.menu_file.add_command(label='Exit', command=self.on_exit) # Adds an option to the menu
        self.menubar.add_cascade(menu=self.menu_file, label='File') # Adds File menu to the bar. Can also be used to create submenus.

        self.menu_help = tk.Menu(self.menubar) #Creates a "Run" menu
        self.menu_help.add_command(label='Compilar', command=self.compile)
        self.menu_help.add_command(label='Compilar y ejecutar', command=self.compileRun)
        self.menubar.add_cascade(menu=self.menu_help, label='Run')

        self.root.bind('<Key>', self.root_key_pressed)

        self.root.config(menu=self.menubar)


class TextLineNumbers(tk.Canvas):
    ''' Encargada de mostrar los números de línea '''
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget
        
    def redraw(self, *args):
        '''dibuja los números de línea'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            lineNum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=lineNum)
            i = self.textwidget.index("%s+1line" % i)

class EventText(tk.Text):
    '''Clase de Text que genera eventos cuando cualquier cosa cambia'''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # avoid error when copying
        if args[0] == 'get' and (args[1] == 'sel.first' and args[2] == 'sel.last') and not self.tag_ranges(
            'sel'): return ''

        # avoid error when deleting
        if args[0] == 'delete' and (args[1] == 'sel.first' and args[2] == 'sel.last') and not self.tag_ranges(
            'sel'): return

        cmd = (self._orig, args[0]) + args[1:]
        result = self.tk.call(cmd)

        if args[0] in ('insert', 'delete', 'replace'):
            self.event_generate('<<Change>>')
        if(args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        return result

class GUI(ttk.Frame):
    """Main GUI class"""
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.init_gui()

    def println(self, text):
        '''Agrega una línea de texto a la ventana de la consola'''
        self.console.insert(tk.END, text)

    def cls(self):
        '''Borra el contenido de la consola'''
        self.console.delete(0,tk.END)

    def _on_change(self, event):
        self.linenumbers.redraw()

    def init_gui(self):
        self.root.title('Robotic Hand')
        self.root.geometry("1200x800")
        self.root.option_add('*tearOff', 'FALSE') # Disables ability to tear menu bar into own window
        
        # Menu Bar
        self.menubar = Menubar(self.root, self)

        # Text box frame
        self.textFrame = tk.Frame(self.root)

        # Scroll Bar
        self.scrollbar = ttk.Scrollbar(self.textFrame)
        # packing the scrollbar function
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text Box
        self.text_box = EventText(self.textFrame, yscrollcommand=self.scrollbar.set)
        self.text_box.bind("<<Change>>", self._on_change)
        self.text_box.bind("<Configure>", self._on_change)

        # Line numbers
        self.linenumbers = TextLineNumbers(self.textFrame, width=25)
        self.linenumbers.attach(self.text_box)

        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
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
            if child == self.linenumbers: continue
            child.configure(padx=10, pady=5)

