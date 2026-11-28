import math
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from functools import partial
import Managers
import time
import threading
import textwrap


class Backup_GUI:
    def __init__(self, server_manager, backup_manager, backup_thread_manager, name, root):
        self.__server_manager = server_manager
        self.__backup_manager = backup_manager
        self.__backup_thread_manager = backup_thread_manager
        self.__name = name
        self.__root = root
        self.__backup_data, self.__last_backup_loaded = backup_manager.load_server_backups_data(name)

        self.__style = Style(theme='superhero')
        self.__window = tk.Toplevel(root)

        # this varible is used to detect if the backup code is running
        self.__text_popup_active = False

        self.__loading_text = "Loading..."
        self.__info_popups = []

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

        self.__window.configure(background='#2b3e50')
        self.__window.title("Backups")
        self.__window.geometry("500x500")

    def display_header(self):
        frame = tk.Frame(self.__window, height=65, width=500, bg='#617ab0')
        frame.place(x=0, y=0)
        if len(self.__name) > 20:
            name = self.__name[0:10]
            name = name + "..."
        else:
            name = self.__name
        if not self.__last_backup_loaded:
            text = "None"
        else:
            text = self.__last_backup_loaded
        l = tk.Label(self.__window, text="last Backup Loaded: " + text, font=("Helvetica", 11, "bold"), bg='#617ab0')
        l.place(x=5, y=40)

        l = tk.Label(self.__window, text=(name), font=("Helvetica", 14, "bold"), bg='#617ab0')
        l.place(x=5, y=5)

        btn = ttk.Button(self.__window, text="Backup",
                         command=partial(self.backup_name_popup, "create"),
                         style='Info.Outline.TButton')
        btn.place(x=400, y=5)

    def Create_info_display(self, title, message):
        InfoPopup = tk.Toplevel(self.__window)
        InfoPopup.configure(background='#2b3e50')
        InfoPopup.geometry("300x200")
        InfoPopup.title(title)

        custom_font = tk.font.Font(family="Arial", size=18)

        # Wrap text at word boundaries
        message = textwrap.fill(message, width=22)

        label = tk.Label(
            InfoPopup,
            text=message,
            bg='#617ab0',
            font=custom_font,
            wraplength=270,
            justify=tk.CENTER
        )
        label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.__info_popups.append(InfoPopup)

    def Destroy_info_display(self):
        for info_popup in self.__info_popups:
            try:
                info_popup.destroy()
            except:
                pass

    def display_backups(self):
        if len(self.__backup_data) > 0:
            for i in range(len(self.__backup_data)):
                frame = ttk.Frame(self.__window, height=43, width=600, style='secondary.Inverse.TLabel')
                frame.place(x=0, y=(48 * i) + 70)

                # name label
                name = self.__backup_data[i]["name"];
                if len(name) > 20:
                    name = name[0:10]
                    name = name + "..."
                l = ttk.Label(self.__window, text=name, style="TLabel")
                l.place(x=5, y=(48 * i) + 80)

                # date label
                date = self.__backup_data[i]["date_created"][0:10]
                l = ttk.Label(self.__window, text=date, style="TLabel")
                l.place(x=40, y=(48 * i) + 80)

                # delete button
                btn = ttk.Button(self.__window, text="Delete",
                                 command=partial(self.delete_backup, self.__name, self.__backup_data[i]["name"]),
                                 style='danger.Outline.TButton')
                btn.place(x=400, y=(48 * i) + 80)

                # load button
                btn = ttk.Button(self.__window, text="Load",
                                 command=partial(self.load_backup, self.__name, self.__backup_data[i]["name"]),
                                 style='success.Outline.TButton')
                btn.place(x=250, y=(48 * i) + 80)

                # copy button
                btn = ttk.Button(self.__window, text="Copy",
                                 command=partial(self.backup_name_popup, "copy", self.__backup_data[i]),
                                 style='info.Outline.TButton')
                btn.place(x=325, y=(48 * i) + 80)

    # this will check for when the backup is made and run nessery commands
    def backup_made(self):
        # this varible is sued to detect if the backup code is running
        self.__text_popup_active = False
        # update display and stop the loop meaning the thread dies
        self.update_backups()
        self.Destroy_info_display()
        self.Create_info_display("Backup Created", "the backup has been successfully created")

    def create_backup(self, paths, server_name, event=None):
        error_duplicate_name = False
        # make sure no duplicate names appear
        for backup in self.__backup_data:
            if backup["name"].lower() == self.__name_entry.get().lower():
                tk.messagebox.showwarning("Warning", "A Backup with this name already exists", master=self.__text_popup)
                # move all the screens to the top again in the right order
                self.__window.attributes('-topmost', True)
                self.__window.attributes('-topmost', False)
                self.__text_popup.attributes('-topmost', True)
                self.__text_popup.attributes('-topmost', False)
                error_duplicate_name = True
        if not error_duplicate_name:
            self.Create_info_display("Loading", "please be patient backup is being made")
            backup_name = self.__name_entry.get()

            self.__text_popup.destroy()
            self.__text_popup_active = False

            self.__backup_thread_manager.add_new_task(self.__name, ["create", [paths, server_name, backup_name, self]])
            # # start thread for creating a backup
            # t = threading.Thread(target=self.__backup_manager.create_backup, args=(paths, server_name, name))
            # t.start()
            # # this will check for when the backup is made and run nessery commands
            # time.sleep(0.1)
            # t2 = threading.Thread(target=self.backup_made)
            # t2.start()



    def delete_backup(self, server_name, backup_name):
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to delete the backup " + backup_name + "?"):
            self.__backup_thread_manager.add_new_task(self.__name, ["delete", [server_name, backup_name, self]])
            #self.__backup_manager.delete_backup(server_name, backup_name)
            #self.update_backups()

        self.__window.attributes('-topmost', True)
        self.__window.attributes('-topmost', False)

    def loading_complete(self):
        # update display and stop the loop meaning the thread dies
        self.update_backups()
        self.Destroy_info_display()
        self.Create_info_display("Loaded Backup", "Backup has been successfully loaded")
        self.__window.attributes('-topmost', True)
        self.__window.attributes('-topmost', False)

    def load_backup(self, server_name, backup_name):
        if tk.messagebox.askyesno("Confirm", "Are you sure you want to load the backup " + backup_name + "?"):
            #self.__backup_manager.load_backup(server_name, backup_name)
            self.Create_info_display("started loading", "backup is being loaded this may take time")

            self.__backup_thread_manager.add_new_task(self.__name, ["load", [server_name, backup_name, self]])

            # t = threading.Thread(target=self.__backup_manager.load_backup, args=(server_name, backup_name))
            # t.start()
            # # this will check for when the backup is made and run nessery commands
            # time.sleep(0.1)
            # t2 = threading.Thread(target=self.loading_complete)
            # t2.start()


        self.__window.attributes('-topmost', True)
        self.__window.attributes('-topmost', False)

    def copy_complete(self):
        pass

    def copy_backup(self, backupvar, event=None):
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
            backup_name = self.__name_entry.get()

            self.__text_popup.destroy()
            self.__backup_thread_manager.add_new_task(self.__name, ["copy", [backupvar, backup_name, self]])
            #self.__backup_manager.copy_backup(backupvar, self.__name_entry.get())

            self.__text_popup_active = False
            #self.update_backups()

    def display(self):
        self.clear_all()
        self.display_header()
        self.display_backups()

    def update_backups(self):
        self.__backup_data, self.__last_backup_loaded = self.__backup_manager.load_server_backups_data(self.__name)
        self.display()

    def clear_all(self):
        # Iterate through every widget inside the frame
        for widget in self.__window.winfo_children():
            widget.destroy()  # deleting widget

    # name is the backup name that would be used for copying or creating backups
    def backup_name_popup(self, type, backup=None):
        # make sure server is no longer running
        if self.__server_manager.find_server(self.__name).get_status() == "closed":
            # make sure another backup isnt already running
            if not self.__text_popup_active:
                self.__text_popup_active = True
                self.__text_popup = tk.Toplevel(self.__window)
                self.__text_popup.configure(background='#2b3e50')
                l = tk.Label(self.__text_popup, text="Enter Backup Name", font=("Helvetica", 14, "bold"), bg='#617ab0')
                l.place(x=5, y=5)
                self.__name_entry = ttk.Entry(self.__text_popup)
                self.__name_entry.place(x=5, y=40)
                self.__name_entry.focus()

                if type == "create":
                    btn = tk.Button(self.__text_popup, text="Backup", command=partial(self.create_backup,
                                                                                      self.__server_manager.get_world_files(
                                                                                          self.__name), self.__name))
                    self.__name_entry.bind("<Return>", partial(self.create_backup,
                                                               self.__server_manager.get_world_files(self.__name),
                                                               self.__name))
                elif type == "copy":
                    btn = tk.Button(self.__text_popup, text="Copy", command=partial(self.copy_backup, backup))
                    self.__name_entry.bind("<Return>", partial(self.copy_backup, backup))
                btn.place(x=5, y=80)
                self.__text_popup.protocol("WM_DELETE_WINDOW", self.text_popup_close)
        else:
            tk.messagebox.showwarning("warning", "unable to create backup's while this server is running")

    def text_popup_close(self):
        self.__text_popup.destroy()
        self.__text_popup_active = False

    def disable_event(self):
        pass
