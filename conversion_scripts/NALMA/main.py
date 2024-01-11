from utils import *
from tools import *
from input import *

base_path = "/home/asubedi/test_cog/"
files = list_directory_files(base_path)
print(files)

def connector(base_path, file_name_type="regular"):
    for_terracotta = True if file_name_type == "terracotta_suitable" else False
    file_names = list_directory_files(base_path)
    for filename in file_names:
        print(f">>> fileName: {filename}", end="\n")
        input_file_path, variable_name, lat_var, lon_var = nalma(base_path, filename)
#         print(input_file_path)
        file = open_file(input_file_path)
        total_data = len(file[variable_name].data)
        for i in range(total_data):
            file = open_file(input_file_path)
            lat, lon, data = copy_lat_lon_data(file, lat_var, lon_var, variable_name, i)
            if check_flashes(data) == True:
                print(data.shape, end=" --> ")
                lat, lon, data = delete_row_col(lat, lon, data)
                print(data.shape)
                lat, lon, data = flip_lat_data(lat, lon, data)
                file = make_new_xarray(lat, lon ,data)
                print(f"Latitude: {file.latitude.shape}, Longitude: {file.longitude.shape}, Data: {file[variable_name].data.shape}")
                generate_cog(file, variable_name, lat_var, lon_var, i, filename, base_path, for_terracotta)
                print("----------------------------------")
            else:
                print(f"No Flashes. FileName: {filename}, i: {i}")
        print("\n")


connector(base_path)