#This self-defined function is used for reading TRMM dataset downloaded from IRI library, 
#and will return time, latitude, longitude and rainfall values in the end

import numpy as np
import netCDF4

def read_trmm(cur_trmm_path,lat_up,lat_down,lon_left,lon_right):

    #Open TRMM path to retreive data
    nc = netCDF4.Dataset(cur_trmm_path);
    prcpvar = nc.variables['precipitation'];
    pdata = prcpvar[:,:,:];

    #Read TRMM time, latitude and longitude
    time_var = nc.variables['T'];
    data_time = netCDF4.num2date(time_var[:],time_var.units);
    data_lat = nc.variables['Y'][:];
    data_lon = nc.variables['X'][:];

    #Store TRMM time to the defined empty list
    trmm_time = [];
    for i in range(0,len(data_time)):
        trmm_time.append(data_time[i].strftime('%Y%m%d'));

    #Calculate borders for the domain
    lat_index1 = np.where(data_lat == data_lat.flat[np.abs(data_lat - lat_down).argmin()]);
    lat_index2 = np.where(data_lat == data_lat.flat[np.abs(data_lat - lat_up).argmin()]); 
    lon_index1 = np.where(data_lon == data_lon.flat[np.abs(data_lon - lon_left).argmin()]);
    lon_index2 = np.where(data_lon == data_lon.flat[np.abs(data_lon - lon_right).argmin()]);  
    L1 = lat_index1[0][0];
    R1 = lat_index2[0][0];
    L2 = lon_index1[0][0];
    R2 = lon_index2[0][0];

    #Calculate TRMM latitude, longitude and rainfall for the domain
    trmm_lat = data_lat[L1:R1];   
    trmm_lon = data_lon[L2:R2];
    trmm_data = pdata[:,L1:R1,L2:R2];

    #Return the calculated values to the main script
    return trmm_time,trmm_lat,trmm_lon,trmm_data;
    nc.close();
