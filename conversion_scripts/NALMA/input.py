import os
import re
import random
import math
import xarray as xa
import numpy as np

from utils import extract_variable_name

def nalma(base_path, filename):
    input_file_path = f"{base_path}{filename}"
    variable_name = extract_variable_name(filename)
    lat='latitude'
    lon='longitude'
    return input_file_path, variable_name, lat, lon

def wtlma(base_path, filename):
    input_file_path = f"{base_path}{filename}"
    variable_name = extract_variable_name(filename)
    lat='latitude'
    lon='longitude'
    return input_file_path, variable_name, lat, lon

def trmm_lis(base_path, filename):
    input_file_path = f'{base_path}{filename}'
    variable_name = "VHRFC_LIS_FRD"
    lat="Latitude"
    lon="Longitude"
    return input_file_path, variable_name, lat, lon