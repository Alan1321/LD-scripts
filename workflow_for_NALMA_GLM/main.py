from input_output import read_nc_file
from nalma import preprocess_nalma
from utils import get_all_nalma_files_in_a_directory, get_all_files_in_a_directory
from glm import preprocess_glm

#NALMA
all_local_nalma_files = get_all_nalma_files_in_a_directory("/home/asubedi/test_cog/")
for each_file_location in all_local_nalma_files:
    #read NALMA netcdf4 file
    file = read_nc_file(each_file_location)
    #define variable that needs to be converted to geotiff 
    variable = "flash_extent"
    #preprocess it for COG conversion
    preprocess_nalma(file, variable, each_file_location).connector()

#GLM
all_local_glm_files = get_all_files_in_a_directory("/home/asubedi/Desktop/data/raw-files/GLM/")
for each_file_location in all_local_glm_files:
    file = read_nc_file(each_file_location)
    variable = 'Flash_extent_density'
    preprocess_glm(file, variable, each_file_location).connector()