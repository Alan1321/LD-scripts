from utils import extract_variable_name, make_directory, extract_file_name
import xarray as xa

def read_nc_file(location):
    return read_local_nc_file(location)

def read_local_nc_file(location):
    #location = /home/asubedi/test_cog/NALMA_20200305_041000_600_10src_0.0109deg-dx_flash_extent.nc
    var_name = extract_variable_name(location)
    file = xa.open_dataset(location, engine="netcdf4", decode_coords='all', decode_times=False)
    return file, var_name

def read_local_nc_file_glm(location):
    #location = /home/asubedi/test_cog/NALMA_20200305_041000_600_10src_0.0109deg-dx_flash_extent.nc
    file = xa.open_dataset(location, engine="netcdf4", decode_coords='all', decode_times=False)
    return file

def read_s3_nc_file(location):
    pass

def output_cog(file, directory_name, filename):
    make_directory(directory_name)
    file.rio.to_raster(f"{directory_name}/{filename}.tif", driver='COG')

