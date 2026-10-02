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

    #currently redundent
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
                json.dump([], f)
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
        with open(self.__metadata_file_path, "r") as f:
            original_data = json.load(f)
            f.close()
        original_data.append(data)
        with open(self.__metadata_file_path, "w") as f:
            json.dump(original_data, f)
            f.close()

    def delete_backup(self, server_name, backup_name):
        with open(self.__metadata_file_path, "r") as f:
            data = json.load(f)
            f.close()

        for i in range(len(data)):
            if data[i]["name"] == backup_name and data[i]["server"] == server_name:
                backup = data.pop(i)
                break

        with open(self.__metadata_file_path, "w") as f:
            json.dump(data, f)
            f.close()

        if backup:
            if os.path.exists(backup["backup_path"]):
                shutil.rmtree(backup["backup_path"])
            else:
                print("The file does not exist")


    def load_backup(self, server_name, backup_name):
        backup = self.find_backup(server_name, backup_name)
        world_files = self.__server_manager.get_world_files(server_name)
        backup_files = os.listdir(backup["backup_path"])
        print(backup_files)
        for file in world_files:
            for backup_file in backup_files:
                ht = os.path.split(file)
                name = ht[1]
                if backup_file == name:
                    shutil.rmtree(file)
                    shutil.copytree(os.path.join(backup["backup_path"], backup_file), file)
                    print("loading world file "+name)
                    break




    def load_server_backups_data(self, name):
        with open(self.__metadata_file_path, "r") as f:
            data = json.load(f)
            f.close()
        backups=[]
        for backup in data:
            if backup["server"] == name:
                backups.append({"name": backup["name"], "backup_path": backup["backup_path"], "date_created": backup["date_created"]})

        return backups

    def find_backup(self, server_name, backup_name):
        with open(self.__metadata_file_path, "r") as f:
            data = json.load(f)
            f.close()
        for backup in data:
            if backup["server"] == server_name and backup["name"] == backup_name:
                return {"name": backup["name"], "backup_path": backup["backup_path"],
                                "date_created": backup["date_created"]}
        return None