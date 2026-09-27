
import threading
import subprocess
import win32con
import win32gui
import time





class Server:
    def __init__(self, name, path, file):
        self.__name  = name
        self.__path = path
        self.__file = file
        self.__status = "Closed"
        self.__terminal = None
        self.__world_files= []
        self.__backups=[]

    def get_name(self):
        return self.__name

    def get_status(self):
        return self.__status

    def start(self):
        self.__status = "running"

        command = "title "
        command = command + self.__name
        command = command + " && java -jar " + self.__file
        if self.__file != "velocity.jar":
            command = command + " --nogui"

        print(command)
        print('r"' + str(self.__path) + '"')
        termninal = subprocess.Popen(
            [
                "cmd.exe",
                "/k",
                command
            ],
            cwd=self.__path,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        self.__terminal = termninal

        t1 = threading.Thread(target=self.minimise_terminal)
        t1.start()

    def stop(self):
        self.__status = "closed"
        if self.__terminal != None:
            subprocess.run([
                "taskkill",
                "/PID",
                str(self.__terminal.pid),
                "/T",  # Kill child processes too
                "/F"  # Force
            ])

    def find_window(self):
        title = ""
        title = title + self.__name
        title = title + "  - java  -jar " + self.__file
        if self.__file != "velocity.jar":
            title = title + " --nogui"

        window = win32gui.FindWindow(None, title)
        return window

    def open_terminal(self):
        window = self.find_window()
        win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
        win32gui.ShowWindow(window, win32con.SW_MAXIMIZE)

    def minimise_terminal(self):
        found = False
        while not found:
            time.sleep(1)
            window = self.find_window()
            if window != 0:
                win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
                found = True

    def set_status(self, status):
        self.__status = status

    def add_world_file(self, world_path):
        self.__world_files.append(world_path)

    def get_world_files(self):
        return self.__world_files