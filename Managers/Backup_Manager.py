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
        self.__metadata_file_path = os.path.join(self.__core_backup_path, "core_metadata.json")


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

        self.metadata_restoration_check()

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
        os.mkdir(final_backup_path)

        #copy files over to backup loaction
        for path in paths:
            end = os.path.split(path)
            shutil.copytree(path, str(os.path.join(final_backup_path, end[1])))


        data={
            "name": backup_name,
            "server": server_name,
            "backup_path": final_backup_path,
            "date_created": datetime.datetime.now().isoformat(),
        }

        self.create_sub_metadata(data, final_backup_path)

        self.append_core_metadata(data)

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

    def metadata_restoration_check(self):
        with open(self.__metadata_file_path, "r") as f:
            core_data = json.load(f)
            f.close()


        sub_data=[]
        for root, dirs, files in os.walk(self.__core_backup_path):
            for file in files:
                if file == "metadata.json":
                    with open(os.path.join(root, file), "r") as f:
                        data = json.load(f)
                        f.close()
                    sub_data.append(data)

        if len(sub_data) > len(core_data):
            loop = len(sub_data)
        else:
            loop = len(core_data)


        #remove core metadata about files that no longer exist
        for c in core_data:
            if not os.path.exists(c["backup_path"]):
                with open(self.__metadata_file_path, "r") as f:
                    data = json.load(f)
                    f.close()

                data.remove(c)

                with open(self.__metadata_file_path, "w") as f:
                    json.dump(data, f)
                    f.close()


        #check to see if core metadat is missing files
        for s in sub_data:
            found=False
            for c in core_data:
                if c["name"] == s["name"] and c["server"] == s["server"]:
                    found = True
            if not found:
                print("missing core data")
                self.append_core_metadata(s)

        #check to find any missing sub metadat files
        for c in core_data:
            found=False
            for s in sub_data:
                if c["name"] == s["name"] and c["server"] == s["server"]:
                    found = True
            if not found:
                print("missing sub data")
                if os.path.exists(s["backup_path"]):
                    self.create_sub_metadata(c, c["backup_path"])




    def append_core_metadata(self, data):
        # load core metadata file
        with open(self.__metadata_file_path, "r") as f:
            original_data = json.load(f)
            f.close()

        # write back to the core metadata file with the new backups data added
        original_data.append(data)
        with open(self.__metadata_file_path, "w") as f:
            json.dump(original_data, f)
            f.close()

    def create_sub_metadata(self, data, path):
        # create the sub metadatafile in final backup path
        with open(os.path.join(path, "metadata.json"), "w") as f:
            json.dump(data, f)
            f.close()

