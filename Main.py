
import sys
import Server_GUI
import Managers.Server_Manager
import Managers.Backup_Manager
import threading
import time
import os

class main:
    def __init__(self):
        self.__server_manager = Managers.Server_Manager.Server_Manager()
        self.__backup_manager = Managers.Backup_Manager.Backup_Manager(self.__server_manager)
        self.__terminal = Server_GUI.Server_GUI(self.__server_manager, self)
        self.__root = self.__terminal.get_root()
        self.__kill_thread = False

        self.__t1 = threading.Thread(target=self.update)
        self.__t1.start()


        self.__root.mainloop()

    def shutdown(self):
        if self.__server_manager.full_shutdown():
            self.__kill_thread=True
            self.__root.destroy()

    def update(self):
        while not self.__kill_thread:
            time.sleep(1)
            if not self.__kill_thread:
                self.__server_manager.check_active_servers()
                self.__terminal.update_status()


    def get_backup_manager(self):
        return self.__backup_manager

    def get_server_manager(self):
        return self.__server_manager

    def get_root(self):
        return self.__root


if __name__ == "__main__":
    mainvar = main()
    sys.exit()

