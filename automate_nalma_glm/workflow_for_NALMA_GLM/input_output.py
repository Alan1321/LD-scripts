from .utils import make_directory
import xarray as xa
import os

def read_nc_file(location):
    return read_local_nc_file(location)

def read_local_nc_file(location):
    file = xa.open_dataset(location, engine="netcdf4", decode_coords='all', decode_times=False)
    return file

def read_s3_nc_file(location):
    pass

def output_cog(file, directory_name, filename, dataset_folder_name):
    path = os.getcwd()
    split = path.split('/')
    BASE_PATH = "/".join(split[:-4]) + '/data'
    make_directory(f"{BASE_PATH}/{dataset_folder_name}")
    make_directory(f"{BASE_PATH}/{dataset_folder_name}/{directory_name}")
    file.rio.to_raster(f"{BASE_PATH}/{dataset_folder_name}/{directory_name}/{filename}.tif", driver='COG')