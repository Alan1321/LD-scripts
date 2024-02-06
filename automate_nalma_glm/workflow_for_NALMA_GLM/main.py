from .input_output import read_nc_file
from .nalma import preprocess_nalma
from .utils import get_all_nalma_files_in_a_directory, get_all_files_in_a_directory, list_files
from .glm import preprocess_glm
import shutil
import glob

# from ..const import BASE_PATH

# BASE_PATH = '/home/ubuntu/'
# BASE_PATH = '/home/asubedi/'

def convert_nalma_glm(BASE_PATH):
    #NALMA
    all_local_nalma_files = list_files(f"{BASE_PATH}data/NALMA_processed/grid_files/")
    print(all_local_nalma_files)
    for each_file_location in all_local_nalma_files:
        #read NALMA netcdf4 file
        file = read_nc_file(each_file_location)
        #define variable that needs to be converted to geotiff 
        variable = "flash_extent"
        #preprocess it for COG conversion
        preprocess_nalma(file, variable, each_file_location).connector()

    #GLM
    all_local_glm_files = get_all_files_in_a_directory(f"{BASE_PATH}data/GLM_input/")
    for each_file_location in all_local_glm_files:
        file = read_nc_file(each_file_location)
        variable = 'Flash_extent_density'
        preprocess_glm(file, variable, each_file_location).connector()


    shutil.rmtree(f"{BASE_PATH}data/NALMA_input/")
    shutil.rmtree(f"{BASE_PATH}data/GLM_input/")
