from input_output import read_nc_file, read_local_nc_file_glm
from nalma import preprocess_nalma
from utils import get_all_files_in_a_directory
from glm import preprocess_glm

# #NALMA
# all_local_nalma_files = get_all_files_in_a_directory("/home/asubedi/test_cog/")
# for location in all_local_nalma_files:
#     #read NALMA netcdf4 file, extract variable 
#     file, variable = read_nc_file(location) 
#     #preprocess it for COG conversion
#     preprocess_nalma(file, variable, location).connector()

#GLM
location = "/home/asubedi/Desktop/data/raw-files/GLM/OR_GLM-L3-GLMF-M6_G16_s202315823490000_e202315823500000_c20231582351080.nc"
file = read_local_nc_file_glm(location)
variable = 'Flash_extent_density'
preprocess_glm(file, variable, location).connector()