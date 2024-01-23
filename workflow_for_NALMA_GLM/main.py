from input_output import read_nc_file
from nalma import preprocess_nalma
from utils import get_all_files_in_a_directory


all_local_nalma_files = get_all_files_in_a_directory("/home/asubedi/test_cog/")

for location in all_local_nalma_files:
    #read NALMA netcdf4 file, extract variable 
    file, variable = read_nc_file(location) 
    #preprocess it for COG conversion
    preprocess_nalma(file, variable, location).connector()




