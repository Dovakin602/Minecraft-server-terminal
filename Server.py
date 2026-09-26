





class Server:
    def __init__(self, name, path, file):
        self.__name  = name
        self.__path = path
        self.__file = file
        self.__status = "Closed"
        self.__terminal = None

    def get_name(self):
        return self.__name

    def get_status(self):
        return self.__status
