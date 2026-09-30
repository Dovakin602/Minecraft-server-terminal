import json
import sys
import os
import shutil
import datetime

class Backup_Manager:
    def __init__(self, server_manager):
        self.__server_manager = server_manager
        self.__core_backup_path=None
        self.__metadata_file_path=None
        self.setup()

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
                if file == "session.lock" and "Backups" not in root:
                    ht = os.path.split(root)
                    name = os.path.split(ht[0])
                    self.__server_manager.add_world_file(name[1], root)

    def setup(self):

        if getattr(sys, 'frozen', False):
            # Running as an .exe
            dir_path = os.path.dirname(sys.executable)
        else:
            # Running as normal Python
            dir_path = os.getcwd()

        self.__core_backup_path = os.path.join(dir_path, "Backups")
        self.__metadata_file_path = os.path.join(self.__core_backup_path, "metadata.json")


        try:
            os.mkdir(self.__core_backup_path)
            print(f"Directory Backups created successfully.")
        except FileExistsError:
            print(f"Directory Backups already exists.")
        except PermissionError:
            print(f"Permission denied: Unable to create Backups.")
        except Exception as e:
            print(f"An error occurred: {e}")


        exists = os.path.exists(self.__metadata_file_path)
        if not exists:
            with open(self.__metadata_file_path, "w") as f:
                json.dump({}, f)
                f.close()




    def create_backup(self, paths, server_name, backup_name):
        folder_name = server_name+"_Backups"
        sever_backups_path = os.path.join(self.__core_backup_path, folder_name)
        exists = os.path.exists(sever_backups_path)
        if not exists:
            try:
                os.mkdir(sever_backups_path)
                print(f"Directory Backups created successfully.")
            except PermissionError:
                print(f"Permission denied: Unable to create Backups.")
            except Exception as e:
                print(f"An error occurred: {e}")
        final_backup_path = os.path.join(sever_backups_path, backup_name)
        print(backup_name)
        print(final_backup_path)
        os.mkdir(final_backup_path)
        for path in paths:
            end = os.path.split(path)
            shutil.copytree(path, str(os.path.join(final_backup_path, end[1])))

        data={
            "name": backup_name,
            "server": server_name,
            "backup_path": final_backup_path,
            "date_created": datetime.datetime.now().isoformat(),
        }
        print(data)
        with open(self.__metadata_file_path, "w") as f:
            json.dump(data, f)
            f.close()




