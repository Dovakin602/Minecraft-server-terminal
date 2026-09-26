
import sys
import Server_GUI
import Managers.Server_Manager

class main:
    def __init__(self):
        self.__server_manager = Managers.Server_Manager.Server_Manager()
        self.__terminal = Server_GUI.Server_GUI(self.__server_manager, self)
        self.__root = self.__terminal.get_root()
        self.__root.mainloop()




    def shutdown(self):
        self.__server_manager.full_shutdown()
        self.__root.destroy()
        sys.exit()







if __name__ == "__main__":
    main()