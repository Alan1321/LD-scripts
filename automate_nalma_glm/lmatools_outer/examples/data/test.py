

import xarray as xa
import os

data_out = 'data/output'
folder_path = 'working/NALMA_20200305_052000_600_10src_0.0109deg-dx_flash_extent.nc'
filenames = []

# Iterate through files in the folder
# for filename in os.listdir(folder_path):
#     # Check if the item is a file (not a subdirectory)
#     if os.path.isfile(os.path.join(folder_path, filename)):
#         filenames.append(os.path.join(folder_path, filename))
#
# print(filenames)

data = xa.open_dataset(folder_path, engine="netcdf4", decode_coords='all', decode_times=False)


for i in data['flash_extent'][0]:
    for j in i:
        if j!= 0:
            print(j)
            break


print('-------------')
