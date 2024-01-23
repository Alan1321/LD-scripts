import re
import os

def extract_variable_name(filename):
    pattern = "[a-zA-Z]_flash[a-zA-Z_]+"
    match = re.findall(pattern, filename)
    return match[0][2:]

def scrape_nalma_directory_name(filename):
    filename = filename.split("/")[-1]
    return filename[0:21]

def extract_file_name(filename):
    filename = filename.split("/")[-1]
    return filename[:-3]

def make_directory(path):
    # path = os.path.join(base_path, directory_name)
    if os.path.exists(path) == False:
        os.mkdir(path)
        return True
    return False