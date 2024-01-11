import os
import re
import random
import math
import xarray as xa
import numpy as np

from utils import *
from input import *

output_file_name = "S2A_20160724_135032_27XVB_B0"

def open_file(input_path):
    return xa.open_dataset(input_path, engine="netcdf4", decode_coords='all', decode_times=False)

def copy_lat_lon_data(file, var_name1, var_name2, var_name3, number=0):
    lat = file[var_name1].data.copy()
    lon = file[var_name2].data.copy()
    data = file[var_name3].data[number].copy()
    return lat, lon, data

def make_new_xarray(lat, lon, data):
    file = xa.Dataset(
        {
            "flash_extent": (["longitude", "latitude"], data),
        },
        coords={
            "longitude": (["longitude"], lon),
            "latitude": (["latitude"], lat),
        },
    )
    return file

def generate_cog(file, variable_name, latitude, longitude, number, filename, base_path, for_terracotta):
    file = file[variable_name]
    file = file.transpose(latitude, longitude)
    file.rio.set_crs('epsg:4326')
    file.rio.set_spatial_dims(x_dim=longitude, y_dim=latitude, inplace=True)
    directory_name = scrape_directory_name(filename)
    make_directory(base_path, 'output')
    make_directory(base_path + '/output/', directory_name)

    output_directory = base_path + 'output/' + directory_name + '/'
    file_name = output_directory + output_file_name + str(number) + '.tif'
    print(file_name)
    file.rio.to_raster(f"{file_name}", driver='COG')
    #file.to_netcdf(f"{file_name}.nc")
    
def delete_row_col(lat, lon, data):
    #finding row with all zeroes    
    zero_row = np.where(np.all(data == 0, axis=1))[0]
    #removing lon with all zeroes
    lon = np.delete(lon, zero_row)
    # Find rows with non-zero elements
    non_zero_rows = np.any(data != 0, axis=1)
    # Filter the array based on non-zero rows
    data = data[non_zero_rows]

    #finding columns with all zeroes
    zero_columns = np.where(np.all(data == 0, axis=0))[0]
    #removing lat with all zeroes
    lat = np.delete(lat, zero_columns)
    # Find rows with non-zero elements
    non_zero_rows = np.any(data != 0, axis=1)
    # Find columns with non-zero elements
    non_zero_columns = np.any(data != 0, axis=0)
    # Filter the array based on non-zero rows and columns
    data = data[non_zero_rows][:, non_zero_columns]
    return lat, lon, data

def flip_lat_data(lat, lon, data):
    lat = lat[::-1]
    data = np.flip(data, axis=1)
    return lat, lon, data

def check_flashes(data):
    count = 0
    for row in data:
        for value in row:
            if value != 0:
                count += 1
    if count == 0:
        return False
    return True