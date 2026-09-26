
import sys
import os
import Server

class Server_Manager:
    def __init__(self):
        self.__Servers=[]
        self.Find_server_files()


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
        if velocity is not None:
            if name == "Velocity" or velocity.get_status() == "running":
                server.start()


    def stop_server(self, name):
        instance = self.find_server(name)
        if instance.get_status() != "closed":
            instance.stop()

    def open_terminal(self, name):
        instance = self.find_server(name)
        instance.open_terminal()