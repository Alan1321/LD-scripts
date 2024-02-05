import math
import numpy as np
import xarray as xa
from .input_output import output_cog

class preprocess_glm():
    def __init__(self, file, variable, location):
        self.file = file
        self.variable = variable
        self.location = location
        self.r_eq, self.r_pol, self.H, self.lon0 = self.extract_variables()
        
    def connector(self):
        lat, lon, data = self.copy_lat_lon_data()
        file = self.generate_new_xarray(lat, lon, data)
        self.generate_cog(file)
    
    def generate_cog(self, file):
        print("generating cog ...")
        file = file[self.variable]
        file = file.transpose('lat', 'lon')
        file.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=True)
        file.rio.crs
        file.rio.set_crs('epsg:4326', inplace=True)

        directory_name, filename = self.extract_file_directory_name(self.location)
        output_cog(file, directory_name, filename)

    def extract_file_directory_name(self, location):
        filename = location.split('/')[-1]
        filename = filename[:-3]
        directory_name = "GLM"

        return directory_name, filename

    def copy_lat_lon_data(self):
        print('copying lat, lon, data ...')
        x_cpy = self.file.x.copy()
        y_cpy = self.file.y.copy()

        lat = np.zeros(self.file.x.size)
        lon = np.zeros(self.file.x.size)
        data = self.file[self.variable].data.copy()

        for i in range(x_cpy.size):
            lat[i], lon[i] = self.calc_lat_lon(x_cpy[i], y_cpy[i])

        _lat = lat.copy()
        _lon = lon.copy()
        _data = self.file[self.variable].data.copy()

        end_index = len(lon)
        for index, value in np.ndenumerate(lon[::-1]):
            end_index -= 1
            if value == -999.0:
                _data = np.delete(_data, end_index, axis=0)
                _lon = np.delete(_lon, end_index)

        end_index = len(lat)
        for index, value in np.ndenumerate(lat[::-1]):
            end_index -= 1
            if value == -999.0:
                _data = np.delete(_data, end_index, axis=1)
                _lat = np.delete(_lat, end_index)

        return _lat, _lon, _data
    
    def generate_new_xarray(self, lat, lon, data):
        file = xa.Dataset(
            data_vars={self.variable: (("lon", "lat"), data)},
            coords={"lon": lon, "lat": lat},
            attrs={"instrument_ID": "GLM-1"}
        )
        return file

    def extract_variables(self):
        #radius of Earth at the equator in meters
        r_eq = self.file['goes_imager_projection'].semi_major_axis
        #radius of Earth at the pole in meters
        r_pol = self.file['goes_imager_projection'].semi_minor_axis
        #distance from satellite to earth center in meters
        H = self.file['goes_imager_projection'].perspective_point_height+r_eq
        #longitude of projection origin in units of radians
        lon0 = self.file['goes_imager_projection'].longitude_of_projection_origin * (math.pi/180.)
        return r_eq, r_pol, H, lon0

    def calc_lat_lon(self, xx,yy):
        #intermediate calculations
        a = (math.sin(xx))**2 + (math.cos(xx))**2 * ((math.cos(yy))**2 + self.r_eq**2/self.r_pol**2*(math.sin(yy))**2)
        b = -2 * self.H * math.cos(xx) * math.cos(yy)
        c = self.H**2 - self.r_eq**2

        if b**2-4*a*c < 0:
            lat = -999.
            lon = -999.
        else:
            #distance from the satellite to point P
            r_s = (-b-math.sqrt(b**2-4*a*c))/2/a

            #derived using satellite location and earth geometry s_x, s_y, s_z
            s_x = r_s * math.cos(xx) * math.cos(yy)
            s_y = -r_s * math.sin(xx)
            s_z = r_s * math.cos(xx) * math.sin(yy)

            #geodetic latitude and longitude for point P
            #math.atan(x) return the arc tangent of x, in radians. The result is between -pi/2 and pi/2
            lat = math.atan(((self.r_eq**2)/(self.r_pol**2)) * (s_z/math.sqrt((self.H-s_x)**2 + s_y**2))) #radians
            lon = self.lon0 - math.atan(s_y/(self.H-s_x)) #radians

            #convert radians to degrees
            lat = lat * 180./math.pi #degree
            lon = lon * 180./math.pi #degree

        return lat, lon