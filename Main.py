
import sys
import Server_GUI
import Managers.Server_Manager
import Managers.Backup_Manager
import threading
import time

class main:
    def __init__(self):
        self.__server_manager = Managers.Server_Manager.Server_Manager()
        self.__backup_manager = Managers.Backup_Manager.Backup_Manager(self.__server_manager)
        self.__terminal = Server_GUI.Server_GUI(self.__server_manager, self)
        self.__root = self.__terminal.get_root()


        t1 = threading.Thread(target=self.update)
        t1.start()

        self.__root.mainloop()

    def shutdown(self):
        if self.__server_manager.full_shutdown():
            self.__root.destroy()
            sys.exit()

    def update(self):
        while True:
            time.sleep(1)
            self.__server_manager.check_active_servers()
            self.__terminal.update_status()

    def get_backup_manager(self):
        return self.__backup_manager

    def get_server_manager(self):
        return self.__server_manager



if __name__ == "__main__":
    main()