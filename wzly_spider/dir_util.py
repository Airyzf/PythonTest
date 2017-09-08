import os
import sys

class DirHelper:
    # def __init__(self,folder,file_name):
    #     self.folder=folder
    #     self.file_name=file_name

    @staticmethod
    def create_folder(folder_name):
        name = os.path.join(sys.path[0], folder_name)
        if not os.path.exists(name):
            os.mkdir(name)
        return name

    @staticmethod
    def create_file_name(folder, file_name):
        name = os.path.join(folder, file_name)
        return name
