from curses import flash
import os
from pickle import TRUE
from re import L
import requests
import validators
import gzip
import shutil
from urllib.parse import urlparse

import math
import xarray as xa
from rio_cogeo import cog_validate
import rioxarray

# Mapping
import matplotlib as mpl
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

'''
    TRMM LIS VHR Climatology Data Set COG conversion and mapping
'''

def gz_decompress(path):
    '''
        Decompresses .gz file
    '''
    nc_path = path[:-3]
    with gzip.open(path, 'rb') as infile:
        with open(nc_path, 'wb') as outfile:
            shutil.copyfileobj(infile, outfile)

    return nc_path

def map_grid(grid):
    '''
        Maps corresponding grid coordinates in the globe
        (Edit to extract lat and lon values from COG instead
            More generalized)
    '''
    crs = ccrs.PlateCarree(central_longitude=0.0)
    plt.figure(figsize=(16,8))
    ax = plt.axes(projection=crs)
    cf = ax.contourf(grid['Longitude'], grid['Latitude'], grid, cmap='jet')
    ax.stock_img()
    ax.coastlines(color='white', alpha=0.5)
    ax.add_feature(cfeature.BORDERS, edgecolor='white', alpha=0.2)

    # Grid and Labels
    gl = ax.gridlines(crs=crs, draw_labels=True, linewidth=0.8, alpha=0.5, color='white', linestyle='--')
    gl.top_labels = None
    gl.right_labels = None
    gl.ylocator = mticker.FixedLocator([-90, -60, -30, 0 ,30, 60, 90])
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    norm = mpl.colors.Normalize(vmin=cf.cvalues.min(), vmax=cf.cvalues.max())
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cf.cmap)
    cbar = plt.colorbar(sm, orientation='horizontal', extend='both', pad=0.05, aspect=50, ticks=cf.levels) 
    cbar.set_label('Mean Flash Rate Density', fontsize=12)
    plt.show()

def validate_cog(path, name):
    '''
        Validates whether passed COG is of correct format
    '''
    assert cog_validate(path), f'{name} is NOT a valid cloud optimized GeoTIFF'
    print (f'{name} is a valid cloud optimized GeoTIFF')

def create_fc_cog(grid, var,third_term, dest_path='./'):
    '''
        Creates a COG for the TRMM Full Climatology
    '''
    print("create_FC_COG")
    #grid = grid[::-1] # Orientation is flipped to the correct position
    rows = grid.to_numpy()[:, :] == 0.
    grid.to_numpy()[rows] = None

    l = grid.coords['Latitude'].data
    l[0] = l[0] + 0.4
    l[len(l)-1] = l[len(l) - 1] - 0.4
    grid.coords['Latitude'] = l

    grid = grid.transpose('Latitude', 'Longitude')
    grid.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
    grid.rio.crs
    grid.rio.set_crs('epsg:4326', inplace=TRUE)
    cog_name = f'{var}_co.tif'
    cog_path = f"{dest_path.rstrip('/')}/{cog_name}"
    grid.rio.to_raster(rf'{cog_path}', driver='COG')
    validate_cog(cog_path, cog_name)
    return grid

def create_spec_cogs(flash_rate_ds, var, third_term,dest_path='./'):
    '''
        Converts specific time data from TRMM .nc files into COGs
        TRMM Climatology Collection (Aside from the full data) contains a third coordinate
            Month, day, season, etc. which aren't actual coordinates
            Seen as raster bands by xarray, which isn't the case
            Separation of each 'band' was implemented
    '''
    #Use either one of these depending on your file

    flash_rate_ds = flash_rate_ds.transpose(third_term, 'Latitude', 'Longitude')
    #flash_rate_ds = flash_rate_ds.transpose('Day_of_year', 'Latitude', 'Longitude')
    #flash_rate_ds = flash_rate_ds.transpose('Month_since_Jan_95', 'Latitude', 'Longitude')
    #flash_rate_ds = flash_rate_ds.transpose('Latitude', 'Longitude')
    grids = []
    ds_type = flash_rate_ds.dims[0]

    for grid in flash_rate_ds:
        grid_index = grid.coords[ds_type].values

        # need to update the last latitude data for this COG to be converted
        l = grid.coords['Latitude'].data
        l[0] = l[0] + 0.4
        l[len(l)-1] = l[len(l) - 1] - 0.4
        grid.coords['Latitude'] = l

        grid.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
        grid.rio.crs
        grid.rio.set_crs('epsg:4326', inplace=TRUE)
        
        # Individual COGs are stored in a folder
        dest_folder = f"{dest_path.rstrip('/')}/{var}_cogs"
        if not os.path.isdir(dest_folder):
            os.mkdir(dest_folder)

        cog_name = f'{var}_{ds_type}_{grid_index}_co.tif'
        cog_path = f'{dest_folder}/{cog_name}'
        grid.rio.to_raster(rf'{cog_path}', driver='COG')
        validate_cog(cog_path, cog_name)

        grids.append(grid)
    
    return grids

def get_path():
    '''
        Prompts for data file
    '''
    query = input("Enter the URL or the data file name that you'd like to convert to COG format.\n")
    #Check query input type 
    if validators.url(query):
        sc = requests.get(query).status_code
        
        if sc == 200: #Authentication has been saved
            os.system(f'wget {query}')
        elif  sc == 401: #Authentication is needed
            user = input('\nEnter your username for the corresponding website.\n')
            os.system(f'wget --user={user} --ask-password --auth-no-challenge --no-check-certificate -i {query}')
        else:
            print('\nInvalid Address.')
            exit(1)
        
        url = urlparse(query)
        return os.path.basename(url.path)

    elif os.path.isdir(query):
        return query

    else:
        print('\nInvalid Input.')
        exit(1)

if __name__ == '__main__':

    f1 = input("Enter file path on your local computer")
    f1_engine = 'pynio'
    f1_var = input("Enter the variable name")
    third_term = input("Enter the last term for your file, example Month? Time? Day_of_Year")

    # Gets flash rate density data
    file = xa.open_dataset(f1, engine=f1_engine, decode_coords='all', decode_times=False)
    #var = f'{path[4:9].upper()}_LIS_FRD'
    var = f1_var
    flash_rate_ds = file[var]

    # COG conversion and corresponding grid mapping
        # *Grid mapping commented out*
        # Destination path is set to current directory
    if var == 'VHRFC_LIS_FRD' or var == 'HRFC_COM_FR':
        grid = create_fc_cog(flash_rate_ds, var, third_term)
        # map_grid(grid)
    else:
        grids = create_spec_cogs(flash_rate_ds, var, third_term)
        # for grid in grids:
        #     map_grid(grid)