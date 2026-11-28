import queue
import threading

# Source - https://stackoverflow.com/a/16506527
# Posted by abarnert, modified by community. See post 'Timeline' for change history
# Retrieved 2026-11-26, License - CC BY-SA 3.0




class Backup_Threads_Manager:
    def __init__(self, server_manager, Backup_Manager):
        self.__Backup_Manager = Backup_Manager
        # a queue of server with tasks that need to be done but a thread hasn't picked up yet
        self.__super_queue = queue.Queue()
        self.__server_queues = {}
        self.__active_servers = {}  # a varbile to check if a thread is correctly executing this servers tasks
        self.__in_super_queue = {} # a variable to check weather this server is waiting in the super queue
        self.__server_manager = server_manager
        self.__servers = self.__server_manager.get_server_names()
        #each server gest a queue for tasks and a variable to check if a thread is currently working on its tasks
        for server in self.__servers:
            self.__server_queues[server] = queue.Queue()
            self.__active_servers[server] = False
            self.__in_super_queue[server] = False

        for i in range(4):
            t = threading.Thread(target=self.worker_thread, daemon=True)
            t.start()






    def worker_thread(self):
        while True:
            server = self.__super_queue.get()
            self.__in_super_queue[server] = False
            self.__active_servers[server] = True # to decalr that a thread has picked up this servers tasks
            current_queue = self.__server_queues[server]

            #loop through the servers tasks until none remain
            while current_queue.qsize() > 0:
                task = current_queue.get()
                response = self.prossess_task(task)
                if response[0]:
                    print(f"Completed task {task[0]} for {server}")
                else:
                    print(f"\033[91mTask {task[0]} Server {server} Error: {response[1]}\033[0m")
            #once all tasks are completed it announces that no threads are working on this server
            self.__active_servers[server] = False



    # tasks  = [task name, [tasks parameters]]
    def prossess_task(self, task):
        if task[0] == "create":
            response = self.__Backup_Manager.create_backup(paths=task[1][0], server_name=task[1][1], backup_name=task[1][2])
            #backup gui may no longer exist if closed
            try:
                backup_gui_manager = task[1][3]
                backup_gui_manager.backup_made()
            except:
                pass

        elif task[0] == "load":
            response = self.__Backup_Manager.load_backup(server_name=task[1][0], backup_name=task[1][1])
            try:
                backup_gui_manager = task[1][2]
                backup_gui_manager.loading_complete()
            except:
                pass

        elif task[0] == "copy":
            response = self.__Backup_Manager.copy_backup(backup=task[1][0], backup_name=task[1][1])
            try:
                backup_gui_manager = task[1][2]
                backup_gui_manager.copy_complete()
            except:
                pass

        elif task[0] == "delete":
            response = self.__Backup_Manager.delete_backup(server_name=task[1][0], backup_name=task[1][1])
            try:
                backup_gui_manager = task[1][2]
                backup_gui_manager.update_backups()
            except:
                pass

        else:
            response = [False, "Unknown task"]

        return response

    #server = name of the server
    #tasks  = [task name, [tasks parameters]]
    def add_new_task(self, server, task):
        self.__server_queues[server].put(task)
        print(f"Added task {task[0]} for {server}")
        #if the server is not already in the queue and not currently being worked on
        if not self.__active_servers[server] and not self.__in_super_queue[server]:
            #super queue is a set and therefore duplicatle entires are already filtered out
            self.__super_queue.put(server)
            self.__in_super_queue[server] = True


