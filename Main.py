
import Server_GUI

class main:
    def __init__(self):
        self.__terminal = Server_GUI.Server_GUI()
        self.__root = self.__terminal.get_root()
        self.__root.mainloop()












if __name__ == "__main__":
    main()