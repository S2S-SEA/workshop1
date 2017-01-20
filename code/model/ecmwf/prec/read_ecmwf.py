#This self-defined function is used for reading ECMWF dataset downloaded from ECMWF S2S library, 
#and will return time, step, latitude, longitude and rainfall values in the end

import numpy as np
import netCDF4

def read_ec(cur_ec_path,lat_up,lat_down,lon_left,lon_right):

    #Open ECMWF path to retreive data
    nc = netCDF4.Dataset(cur_ec_path);
    prcpvar = nc.variables['precip'];
    pdata = prcpvar[:,:,:,:];

    #Read ECMWF time, step, latitude and longitude
    time_var = nc.variables['time'];
    data_time = netCDF4.num2date(time_var[:],time_var.units);
    data_step = nc.variables['step'][:];
    data_lat = nc.variables['latitude'][:];
    data_lon = nc.variables['longitude'][:];
    ec_time = data_time;
    ec_step = data_step;

    #Calculate borders for the domain
    lat_index1 = np.where(data_lat == data_lat.flat[np.abs(data_lat - lat_up).argmin()]);
    lat_index2 = np.where(data_lat == data_lat.flat[np.abs(data_lat - lat_down).argmin()]); 
    lon_index1 = np.where(data_lon == data_lon.flat[np.abs(data_lon - lon_left).argmin()]);
    lon_index2 = np.where(data_lon == data_lon.flat[np.abs(data_lon - lon_right).argmin()]);  
    L1 = lat_index1[0][0];
    R1 = lat_index2[0][0];
    L2 = lon_index1[0][0];
    R2 = lon_index2[0][0];

    #Calculate ECMWF latitude, longitude and rainfall for the domain
    ec_lat = data_lat[L1:R1];   
    ec_lon = data_lon[L2:R2];
    ec_data = pdata[:,:,L1:R1,L2:R2];

    #Return the calculated values to the main script
    return ec_time,ec_step,ec_lat,ec_lon,ec_data;
    nc.close();
