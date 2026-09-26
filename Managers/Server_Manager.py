
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

    def get_servers(self):
        return self.__Servers

    def start_server(self):
        return "Server started"

    def stop_server(self):
        return "Server stopped"

    def open_terminal(self):
        return "Open Terminal"