
import sys
import os
import Server
from tkinter import messagebox

class Server_Manager:
    def __init__(self):
        self.__Servers=[]
        self.Find_server_files()

        #resets error counter
        self.__normal_counter=0
        #ensures severs arent toggled to incorrect statueses
        self.__error_counter=0




    def Find_server_files(self):
        if getattr(sys, 'frozen', False):
            # Running as an .exe
            dir_path = os.path.dirname(sys.executable)
        else:
            # Running as normal Python
            dir_path = os.getcwd()


        # locate all server.jar and velocity.jar files
        # and create a server instance for each one
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file == "server.jar" or file == "velocity.jar":
                    ht = os.path.split(root)
                    if file != "velocity.jar":
                        server_instance = Server.Server(ht[1], root, file)
                    else:
                        server_instance = Server.Server("Velocity", root, file)
                    self.__Servers.append(server_instance)

    def get_server_names(self):
        server_names = []
        for server in self.__Servers:
            server_names.append(server.get_name())
        return server_names

    def find_server(self, name):
        for server in self.__Servers:
            if server.get_name() == name:
                return server
        return None

    def get_servers(self):
        return self.__Servers

    def start_server(self, name):
        server = self.find_server(name)
        velocity = self.find_server("Velocity")
        if server.get_status()!="running":
            if velocity is not None:
                if name == "Velocity" or velocity.get_status() == "running":
                    server.start()
                else:
                    messagebox.showwarning("warning", "please start velocity first")
            else:
                server.start()
        else:
            messagebox.showwarning("warning", "this server already running")

    def stop_server(self, name):
        instance = self.find_server(name)
        if instance.get_status() != "closed":
            instance.stop()
        else:
            messagebox.showwarning("warning", "this server already closed")

    def open_terminal(self, name):
        instance = self.find_server(name)
        instance.open_terminal()

    def full_shutdown(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to shutdown?"):
            for server in self.__Servers:
                server.stop()

    def check_active_servers(self):
        self.__normal_counter += 1
        if self.__normal_counter > 2:
            self.__normal_counter = 0
            self.__error_counter = 0

        for instance in self.__Servers:
            if instance.get_status() == "running":
                if instance.find_window() == 0:
                    self.__error_counter += 1
                    if self.__error_counter > 1:
                        self.__error_counter = 0
                        instance.set_status("closed")


    def add_world_file(self, name, world_path):
        server = self.find_server(name)
        server.add_world_file(world_path)