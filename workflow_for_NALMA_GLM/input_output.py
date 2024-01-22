from utils import extract_variable_name
import xarray as xa

def read_nc_file(location):
    return read_local_nc_file(location)

def read_local_nc_file(location):
    #location = /home/asubedi/test_cog/NALMA_20200305_041000_600_10src_0.0109deg-dx_flash_extent.nc
    var_name = extract_variable_name(location)
    file = xa.open_dataset(location, engine="netcdf4", decode_coords='all', decode_times=False)
    return file, var_name

def read_s3_nc_file(location):
    pass