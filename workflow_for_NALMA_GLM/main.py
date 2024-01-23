from input_output import read_nc_file
from nalma import preprocess_nalma

#define file location
location = "/home/asubedi/test_cog/NALMA_20200305_041000_600_10src_0.0109deg-dx_flash_extent.nc"
#read NALMA netcdf4 file, extract variable 
file, variable = read_nc_file(location) 
#preprocess it for COG conversion
preprocess_nalma(file, variable, location).connector()



