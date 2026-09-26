import subprocess
import time
import os
from ttkbootstrap import Style
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import threading
import Utils
import sys

class Server_GUI:
    def __init__(self):
        self.__style = Style(theme='superhero')
        self.__root = self.__style.master
        self.config()


        self.__ipAddr = Utils.get_ip()

        self.display()


    def config(self):
        self.__style.configure('TLabel', background='#050d42')
        self.__style.configure('danger.TLabel', background='#050d42')
        self.__style.configure('secondary.Inverse.TLabel', background='#050d42')
        self.__style.configure('success.Outline.TButton', background="#31383F")
        self.__style.configure('danger.Outline.TButton', background='#31383F')
        self.__style.configure('info.Outline.TButton', background='#31383F')

        self.__root.title("server setup")
        self.__root.geometry("700x400")


    def display_ip(self):
        l = ttk.Label(self.__root, text=("ip address: " + self.__ipAddr), font=("Helvetica", 14, "bold"),style='info.Outline.TButton')
        l.place(x=5, y=0)

    def display_servers(self):
        for i in range(len(self.__servers)):
            frame = ttk.Frame(self.__root, height=43, width=600, style='secondary.Inverse.TLabel')
            frame.place(x=0, y=(48 * i) + 38)

            # creating buttons
            btn = ttk.Button(self.__root, text="Start", command=partial(self.start_server, self.__servers[i].get_name()),
                             style='success.Outline.TButton')
            btn.place(x=5, y=(48 * i) + 45)
            btn = ttk.Button(self.__root, text="Stop", command=partial(self.stop_server, self.__servers[i].get_name()),
                             style='danger.Outline.TButton')
            btn.place(x=80, y=(48 * i) + 45)
            btn = ttk.Button(self.__root, text="Terminal", command=partial(self.open_server, self.__servers[i].get_name()),
                             style='info.Outline.TButton')
            btn.place(x=145, y=(48 * i) + 45)

            name = self.__servers[i].get_name()
            if len(name) > 20:
                name = name[0:10]
                name = name + "..."

            # name label
            l = ttk.Label(self.__root, text=name, style="TLabel")
            l.place(x=265, y=(48 * i) + 50)
            # status lable
            l = ttk.Label(self.__root, text=self.__servers[i].get_status(), style='danger.TLabel')
            l.place(x=475, y=(48 * i) + 50)
            self.__status_labels[self.__servers[i].get_name()] = l

        hight = 49 * (len(self.__servers) + 1)
        string = "600x" + str(hight)
        self.__root.geometry(string)

    def display(self):
        self.display_ip()

    def get_root(self):
        return self.__root
