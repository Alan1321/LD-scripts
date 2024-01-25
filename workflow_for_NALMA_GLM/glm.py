import math

class preprocess_glm():
    def __init__(self, file, variable, location):
        self.file = file
        self.r_eq, self.r_pol, self.H, self.lon0 = self.extract_variables()
        
    def connector(self):
        pass

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

    def calc_lat_lon(xx,yy):
        #intermediate calculations
        a = (math.sin(xx))**2 + (math.cos(xx))**2 * ((math.cos(yy))**2 + r_eq**2/r_pol**2*(math.sin(yy))**2)
        b = -2 * H * math.cos(xx) * math.cos(yy)
        c = H**2 - r_eq**2

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
            lat = math.atan(((r_eq**2)/(r_pol**2)) * (s_z/math.sqrt((H-s_x)**2 + s_y**2))) #radians
            lon = lon0 - math.atan(s_y/(H-s_x)) #radians

            #convert radians to degrees
            lat = lat * 180./math.pi #degree
            lon = lon * 180./math.pi #degree

        return lat, lon