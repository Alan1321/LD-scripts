from curses import flash
import os
from pickle import TRUE
from re import L
import requests
import validators
import gzip
import shutil
from urllib.parse import urlparse

import sys
import math
import xarray as xa
import numpy as np
from rio_cogeo import cog_validate
import rioxarray

# Mapping
import matplotlib as mpl
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker

#constants

def convert_to_cog(f2='None',f2_engine='netcdf4'):
    file2 = xa.open_dataset(f2, engine=f2_engine, decode_coords='all', decode_times=False)

    grid = file2.lightning_area_density_index

    data = grid.data
    lat = np.copy(file2.lightning_area_density_index.lightning_area_lat.data)
    lon = np.copy(file2.lightning_area_density_index.lightning_area_lon.data)
    lat_len = len(grid.lightning_area_lat)
    lon_len = len(grid.lightning_area_lat)

    npData = np.zeros((lat_len, lon_len))

    sorted_lat = np.sort(lat, axis=0)
    sorted_lon = np.sort(lon, axis=0)
    npData2 = np.zeros((lat_len, lon_len))

    index = 0
    for i in range (lat_len):
        for j in range(lon_len):
            if(i == j):
                npData[i][j] = data[index]
                index = index + 1


    #function here which returns value given lat and lon
    def get_lat_index(lat_value):
        index = 0
        for i in range(lat_len):
            if(lat[index] == lat_value):
                return index
            else:
                index = index + 1

    def get_lon_index(lon_value):
        index = 0
        for i in range(lon_len):
            if(lon[index] == lon_value):
                return index
            else:
                index = index + 1

    def get_value(lat, lon):
        value = npData[get_lat_index(lat)][get_lon_index(lon)]
        (value != 0) and print(f"lat: {lat}, lon:{lon}, value:{value}")
        return value

    #create new grid here
    for i in range(lat_len):
        for j in range(lon_len):
            npData2[i][j] = get_value(sorted_lat[i], sorted_lon[j])


    finalFile = xa.DataArray(
        data = npData2,
        dims=("Latitude", "Longitude"),
        coords={
            "Latitude":sorted_lat,
            "Longitude":sorted_lon
        },
        attrs=dict(
            description="Ambient temperature.",
            units="degC",
        ),
    )

    finalFile = finalFile.transpose('Latitude', 'Longitude')
    finalFile.rio.set_spatial_dims(x_dim='Longitude', y_dim='Latitude', inplace=True)
    finalFile.rio.crs
    finalFile.rio.set_crs('epsg:4326', inplace=TRUE)


convert_to_cog("/home/asubedi/Desktop/Jupyter-Demo/ISS_LIS_SC_V2.1_20221009_095152_NQC.nc", "netcdf4")