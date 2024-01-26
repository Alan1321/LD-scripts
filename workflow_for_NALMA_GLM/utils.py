import re
import os

def make_directory(path):
    # path = os.path.join(base_path, directory_name)
    if os.path.exists(path) == False:
        os.mkdir(path)
        return True
    return False

def get_all_nalma_files_in_a_directory(directory_path):
    files = []
    for f in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, f)) and f[0:5] == 'NALMA':
            files.append(os.path.join(directory_path, f))
    return files

def get_all_files_in_a_directory(directory_path):
    files = []
    for f in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, f)):
            files.append(os.path.join(directory_path, f))
    return files