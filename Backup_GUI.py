
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
        self.__backup_data=backup_manager.load_server_backups_data(name)

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

    def display_backups(self):
        if len(self.__backup_data) > 0:
            for i in range(len(self.__backup_data)):
                frame = ttk.Frame(self.__window, height=43, width=600, style='secondary.Inverse.TLabel')
                frame.place(x=0, y=(48 * i) + 38)

                # name label
                name=self.__backup_data[i]["name"];
                if len(name) > 20:
                    name = name[0:10]
                    name = name + "..."
                l = ttk.Label(self.__window, text=name, style="TLabel")
                l.place(x=5, y=(48 * i) + 50)


                # date label
                date = self.__backup_data[i]["date_created"][0:10]
                l = ttk.Label(self.__window, text=date, style="TLabel")
                l.place(x=40, y=(48 * i) + 50)

                #delete button
                btn = ttk.Button(self.__window, text="Delete",
                                 command=partial(self.delete_backup, self.__name, self.__backup_data[i]["name"]),
                                 style='danger.Outline.TButton')
                btn.place(x=400, y=(48 * i) + 50)

                # load button
                btn = ttk.Button(self.__window, text="Load",
                                 command=partial(self.load_backup, self.__name, self.__backup_data[i]["name"]),
                                 style='success.Outline.TButton')
                btn.place(x=300, y=(48 * i) + 50)

    def create_backup(self, paths, server_name):
        error_duplicate_name = False
        for backup in self.__backup_data:
            if backup["name"].lower() == self.__name_entry.get().lower():
                tk.messagebox.showwarning("Warning", "A Backup with this name already exists", master=self.__text_popup)
                self.__window.attributes('-topmost', True)
                self.__window.attributes('-topmost', False)
                self.__text_popup.attributes('-topmost', True)
                self.__text_popup.attributes('-topmost', False)
                error_duplicate_name = True
        if not error_duplicate_name:
            self.__backup_manager.create_backup(paths, server_name, self.__name_entry.get())
            self.__text_popup.destroy()
            self.__text_popup_active = False
            self.update_backups()

    def delete_backup(self, server_name, backup_name):
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to delete the backup "+backup_name+"?"):
            self.__backup_manager.delete_backup(server_name, backup_name)
            self.update_backups()

            self.__window.attributes('-topmost', True)
            self.__window.attributes('-topmost', False)

    def load_backup(self, server_name, backup_name):
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to load the backup " + backup_name + "?"):
            self.__backup_manager.load_backup(server_name, backup_name)

            self.__window.attributes('-topmost', True)
            self.__window.attributes('-topmost', False)

    def display(self):
        self.clear_all()
        self.display_header()
        self.display_backups()

    def update_backups(self):
        self.__backup_data = self.__backup_manager.load_server_backups_data(self.__name)
        self.display()

    def clear_all(self):
        # Iterate through every widget inside the frame
        for widget in self.__window.winfo_children():
            widget.destroy() # deleting widget

    def backup_name_popup(self):
        if self.__server_manager.find_server(self.__name).get_status()=="closed":
            if not self.__text_popup_active:
                self.__text_popup_active = True
                self.__text_popup = tk.Toplevel(self.__window)
                l = tk.Label(self.__text_popup, text="Enter Backup Name", font=("Helvetica", 14, "bold"), bg='#617ab0')
                l.place(x=5, y=5)
                self.__name_entry = ttk.Entry(self.__text_popup)
                self.__name_entry.place(x=5, y=40)
                btn = tk.Button(self.__text_popup, text="Backup",command=partial(self.create_backup,self.__server_manager.get_world_files(self.__name), self.__name))
                btn.place(x=5, y=80)
                self.__text_popup.protocol("WM_DELETE_WINDOW", self.text_popup_close)
        else:
            tk.messagebox.showwarning("warning", "unable to create backup's while this server is running")

    def text_popup_close(self):
        self.__text_popup.destroy()
        self.__text_popup_active = False
