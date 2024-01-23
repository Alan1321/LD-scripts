import xarray as xa
import numpy as np
from utils import extract_file_name, scrape_nalma_directory_name
from input_output import output_cog

class preprocess_nalma():
    def __init__(self, file, variable, location):
        self.latitude = 'latitude'
        self.longitude = 'longitude'
        self.variable = variable
        self.file = file
        self.location = location
    
    def connector(self):
        total_grids = len(self.file[self.variable].data)
        print(f"total_grids: {total_grids}")
        for grid_number in range(total_grids):
            lat, lon, data = self.copy_lat_lon_data(self.file, number=grid_number)
            if self.check_flashes(data):
                lat, lon, data = self.delete_row_col(lat, lon, data)
                lat, lon, data = self.flip_lat_data(lat, lon, data)
                new_file = self.make_new_xarray(lat, lon, data)
                self.generate_cog(new_file, grid_number)
            else:
                print(f"### ### ### No flashes on file: {extract_file_name(self.location)}_{grid_number}")
                continue

    def copy_lat_lon_data(self, file, number=0):
        lat = file[self.latitude].data.copy()
        lon = file[self.longitude].data.copy()
        data = file[self.variable].data[number].copy()
        return lat, lon, data
    
    def make_new_xarray(self, lat, lon, data):
        file = xa.Dataset(
            {
                self.variable: ([self.longitude, self.latitude], data),
            },
            coords={
                self.longitude: ([self.longitude], lon),
                self.latitude: ([self.latitude], lat),
            },
        )
        return file
    
    def generate_cog(self, file, grid_number):
        file = file[self.variable]
        file = file.transpose(self.latitude, self.longitude)
        file.rio.set_crs('epsg:4326')
        file.rio.set_spatial_dims(x_dim=self.longitude, y_dim=self.latitude, inplace=True)

        directory_name = scrape_nalma_directory_name(self.location)
        filename = extract_file_name(self.location) + f"_{grid_number}"
        output_cog(file, directory_name, filename)

    def delete_row_col(self, lat, lon, data):
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
    
    def flip_lat_data(self, lat, lon, data):
        lat = lat[::-1]
        data = np.flip(data, axis=1)
        return lat, lon, data

    def check_flashes(self, data):
        count = 0
        for row in data:
            for value in row:
                if value != 0:
                    count += 1
        if count == 0:
            return False
        return True