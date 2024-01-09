import os
import requests
import validators
import gzip
import shutil
from urllib.parse import urlparse

import xarray as xa
from rio_cogeo import cog_validate

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

def create_fc_cog(grid, var, dest_path='./'):
    '''
        Creates a COG for the TRMM Full Climatology
    '''
    grid = grid[::-1] # Orientation is flipped to the correct position
    rows = grid.to_numpy()[:, :] == 0.
    grid.to_numpy()[rows] = None
        
    grid.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
    grid.rio.crs
    grid.rio.set_crs('epsg:4326')

    cog_name = f'{var}_co.tif'
    cog_path = f"{dest_path.rstrip('/')}/{cog_name}"
    grid.rio.to_raster(rf'{cog_path}', driver='COG')
    validate_cog(cog_path, cog_name)

    return grid

def create_spec_cogs(flash_rate_ds, var, dest_path='./'):
    '''
        Converts specific time data from TRMM .nc files into COGs
        TRMM Climatology Collection (Aside from the full data) contains a third coordinate
            Month, day, season, etc. which aren't actual coordinates
            Seen as raster bands by xarray, which isn't the case
            Separation of each 'band' was implemented
    '''
    grids = []
    ds_type = flash_rate_ds.dims[0]

    for grid in flash_rate_ds:
        grid = grid[::-1] # Orientation is flipped to the correct position
        rows = grid.to_numpy()[:, :] == 0.
        grid.to_numpy()[rows] = None
        grid_index = grid.coords[ds_type].values

        grid.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
        grid.rio.crs
        grid.rio.set_crs('epsg:4326')

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

    # Check query input type 
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

    path = get_path()
    if path[-3:] == '.gz':
        path = gz_decompress(path)

    # Gets flash rate density data
    file = xa.open_dataset(path, engine='netcdf4', decode_coords='all')
    var = f'{path[4:9].upper()}_LIS_FRD'
    flash_rate_ds = file[var]

    # COG conversion and corresponding grid mapping
        # *Grid mapping commented out*
        # Destination path is set to current directory
    if var == 'VHRFC_LIS_FRD':
        grid = create_fc_cog(flash_rate_ds, var)
        # map_grid(grid)
    else:
        grids = create_spec_cogs(flash_rate_ds, var)
        # for grid in grids:
        #     map_grid(grid)
