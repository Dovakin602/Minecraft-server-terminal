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

    def display(self):
        self.display_ip()

    def get_root(self):
        return self.__root
