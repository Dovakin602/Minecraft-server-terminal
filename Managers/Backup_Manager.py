

import sys
import os


class Backup_Manager:
    def __init__(self, server_manager):
        self.__server_manager = server_manager

        self.find_world_files()

    def find_world_files(self):
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
                if file == "session.lock":
                    ht = os.path.split(root)
                    name = os.path.split(ht[0])
                    self.__server_manager.add_world_file(name[1], root)

