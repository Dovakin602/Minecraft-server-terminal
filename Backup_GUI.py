
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from functools import partial

class Backup_GUI:
    def __init__(self, server_manager, backup_manager, name, root):
        self.__server_manager = server_manager
        self.__backup_manager = backup_manager
        self.__name = name
        self.__root = root

        self.__style = Style(theme='superhero')
        self.__window = tk.Toplevel(root)
        self.__text_popup_active=False

        self.config()
        self.display()


    def config(self):

        self.__style.configure('TLabel', background='#050d42')
        self.__style.configure('danger.TLabel', background='#050d42')
        self.__style.configure('success.TLabel', background='#050d42')
        self.__style.configure('secondary.Inverse.TLabel', background='#050d42')
        self.__style.configure('success.Outline.TButton', background="#31383F")
        self.__style.configure('danger.Outline.TButton', background='#31383F')
        self.__style.configure('info.Outline.TButton', background='#31383F')

        self.__window.configure(background='#313d57')
        self.__window.title("Backups")
        self.__window.geometry("500x500")

    def display_header(self):
        frame = tk.Frame(self.__window, height=43, width=500, bg='#617ab0')
        frame.place(x=0, y=0)
        if len(self.__name) > 20:
            name = self.__name[0:10]
            name = name + "..."
        else:
            name = self.__name
        l = tk.Label(self.__window, text=(name), font=("Helvetica", 14, "bold"), bg='#617ab0')
        l.place(x=5, y=5)

        btn = ttk.Button(self.__window, text="Backup",
                         command=partial(self.backup_name_popup,),
                         style='Info.Outline.TButton')
        btn.place(x=400, y=5)

    def create_backup(self, paths, server_name):
        self.__backup_manager.create_backup(paths, server_name, self.__name_entry.get())
        self.__text_popup.destroy()
        self.__text_popup_active = False

    def display(self):
        self.display_header()

    def backup_name_popup(self):
        if not self.__text_popup_active:
            self.__text_popup_active = True
            self.__text_popup = tk.Toplevel(self.__window)
            l = tk.Label(self.__text_popup, text="Enter Backup Name", font=("Helvetica", 14, "bold"), bg='#617ab0')
            l.place(x=5, y=5)
            self.__name_entry = ttk.Entry(self.__text_popup)
            self.__name_entry.place(x=5, y=40)
            btn = tk.Button(self.__text_popup, text="Backup",command=partial(self.create_backup,self.__server_manager.get_world_files(self.__name), self.__name))
            btn.place(x=5, y=80)
