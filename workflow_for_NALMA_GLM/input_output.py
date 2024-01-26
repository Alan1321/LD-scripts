from utils import make_directory
import xarray as xa

def read_nc_file(location):
    return read_local_nc_file(location)

def read_local_nc_file(location):
    file = xa.open_dataset(location, engine="netcdf4", decode_coords='all', decode_times=False)
    return file

def read_s3_nc_file(location):
    pass

def output_cog(file, directory_name, filename):
    make_directory(directory_name)
    file.rio.to_raster(f"{directory_name}/{filename}.tif", driver='COG')