import os
import re
import random
import math
import xarray as xa
import numpy as np

def make_directory(base_path, directory_name):
    path = os.path.join(base_path, directory_name)
    if os.path.exists(path) == False:
        os.mkdir(path)
        return True
    return False

def scrape_directory_name(filename):
    #name=f"S2A_20160724_135032_27XVB_B{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{number}.tif"
    return filename[0:21]

#get all file names from a directory
#TODO: rename it to list directory nc files
def list_directory_files(path):
    dir_list = os.listdir(path)
    files = [f for f in dir_list if os.path.isfile(path+'/'+f)]
    files = [f for f in files if f[len(f)-3:] == ".nc"]
    return files

def extract_variable_name(filename):
    pattern = "[a-zA-Z]_flash[a-zA-Z_]+"
    match = re.findall(pattern, filename)
    return match[0][2:]