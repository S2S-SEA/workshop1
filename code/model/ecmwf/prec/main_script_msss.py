#This main script processes the downloaded ECMWF and TRMM dataset to generate mean square skill score (MSSS) for each individual model lead time. 
#Self-defined functions "read_ecmwf", "read_trmm" and "plot_figure_msss" are used to read ECMWF and TRMM dataset and for final visualization.

import datetime
import numpy as np
import netCDF4
from scipy import interpolate
import read_trmm
import read_ecmwf
import plot_figure_msss

#Model initial dates, years and steps
model_initial_date = ['1013','1017','1020','1024','1027','1031','1103','1107','1110','1114','1117','1121','1124'];
start_year = 1998;
end_year = 2014;
model_step = 4;

#Specify target month
target_month = '11';

#Specify the domain
lat_up = 30;
lat_down = -20;
lon_left = 80;
lon_right = 150;

#Define ECMWF and TRMM data path
ec_input = '.../data/model/ecmwf/prec';
trmm_input = '.../data/obs/prec';
trmm_filename = 'TRMM_Daily_Nov_1998-2014.nc';
cur_trmm_path = trmm_input + '/' + trmm_filename;

#Call function "read_trmm" to read TRMM dataset and return time, latitude, longitude and rainfall values
trmm_time,trmm_lat,trmm_lon,trmm_data = read_trmm.read_trmm(cur_trmm_path,lat_up,lat_down,lon_left,lon_right);

#Read ECMWF latitude and longitude for TRMM interpolation
nc = netCDF4.Dataset(ec_input + '/' + 'ECMWF_prec_2016-10-13_weekly.nc');
data_lat = nc.variables['latitude'][:];
data_lon = nc.variables['longitude'][:];
lat_index1 = np.where(data_lat == data_lat.flat[np.abs(data_lat - lat_up).argmin()]);
lat_index2 = np.where(data_lat == data_lat.flat[np.abs(data_lat - lat_down).argmin()]); 
lon_index1 = np.where(data_lon == data_lon.flat[np.abs(data_lon - lon_left).argmin()]);
lon_index2 = np.where(data_lon == data_lon.flat[np.abs(data_lon - lon_right).argmin()]);  
L1 = lat_index1[0][0];
R1 = lat_index2[0][0];
L2 = lon_index1[0][0];
R2 = lon_index2[0][0];
ec_lat = data_lat[L1:R1];   
ec_lon = data_lon[L2:R2];
nc.close();

#Interpolate TRMM to ECMWF resolution
trmm_new_data = np.zeros([len(trmm_time),len(ec_lat),len(ec_lon)]);
for i_time in range(0,len(trmm_time)):
    pi = interpolate.interp2d(trmm_lon,trmm_lat,trmm_data[i_time,:,:]);
    ec_lat2 = ec_lat[::-1];
    trmm_data_temp = pi(np.asarray(ec_lon),np.asarray(ec_lat2));
    trmm_new_data[i_time,:,:] = np.flipud(trmm_data_temp);

#For each model time step
for i_step in range(0,model_step):
    sum_ec_trmm = np.zeros([len(ec_lat),len(ec_lon)]);
    sum_trmm = np.zeros([len(ec_lat),len(ec_lon)]);

    #For each model initial date
    for i_date in range(0,len(model_initial_date)):
        model_date = model_initial_date[i_date];

        #Find the corresponding data file for each initial date
        cur_ec_filename = 'ECMWF_prec_2016-' + model_date[:2] + '-' + model_date[-2:] + '_weekly.nc'
        cur_ec_path = ec_input + '/' + cur_ec_filename;

        #Call function "read_ecmwf" to read ECMWF dataset and return time, step, latitude, longitude and rainfall values
        ec_time,ec_step,ec_lat,ec_lon,ec_data = read_ecmwf.read_ec(cur_ec_path,lat_up,lat_down,lon_left,lon_right);
        ec_week_all = np.zeros([len(ec_lat),len(ec_lon)]);
        trmm_week_all = np.zeros([len(ec_lat),len(ec_lon)]);
        index_ec = 0;
        index_trmm = 0;

        #Calculate python datetime for future date
        for i_year in range(start_year,end_year+1):
            pre_date = ec_time[i_year-start_year] + datetime.timedelta(hours=int(ec_step[i_step])-24);
            start_date = pre_date - datetime.timedelta(days=6);
            end_date = pre_date;

            #Check if the dates are within target month
            if start_date.month == int(target_month) and end_date.month == int(target_month):

               #Find corresponding ECMWF data
               ec_week_all = ec_week_all + ec_data[i_year-start_year,i_step,:,:];
               index_ec = index_ec + 1;

               #Find corresponding time index to read corresponding TRMM data
               trmm_day_all = np.zeros([len(ec_lat),len(ec_lon)]);
               for i_day in range(0,7):
                   cur_date = start_date + datetime.timedelta(days=i_day);
                   time_index = trmm_time.index("%04d"%cur_date.year + "%02d"%cur_date.month + "%02d"%cur_date.day);
                   trmm_day_all = trmm_day_all + trmm_new_data[time_index,:,:];
               trmm_week_year = trmm_day_all/7;
               trmm_week_all = trmm_week_all + trmm_week_year;
               index_trmm = index_trmm + 1;

        #Calculate ECMWF weekly climatology
        if index_ec != 0:
           ec_week_climatology = ec_week_all/index_ec;

        #Calculate TRMM weekly climatology
        if index_trmm != 0:
           trmm_week_climatology = trmm_week_all/index_trmm;

        #Calculate python datetime for future date
        for i_year in range(start_year,end_year+1):
            pre_date = ec_time[i_year-start_year] + datetime.timedelta(hours=int(ec_step[i_step])-24);
            start_date = pre_date - datetime.timedelta(days=6);
            end_date = pre_date;

            #Check if the dates are within target month
            if start_date.month == int(target_month) and end_date.month == int(target_month):

               #Find corresponding ECMWF data
               ec_week_year = ec_data[i_year-start_year,i_step,:,:];

               #Find corresponding time index to read corresponding TRMM data
               trmm_day_all = np.zeros([len(ec_lat),len(ec_lon)]);
               for i_day in range(0,7):
                   cur_date = start_date + datetime.timedelta(days=i_day);
                   time_index = trmm_time.index("%04d"%cur_date.year + "%02d"%cur_date.month + "%02d"%cur_date.day);
                   trmm_day_all = trmm_day_all + trmm_new_data[time_index,:,:];
               trmm_week_year = trmm_day_all/7;

               #Calculate intermediate items
               sum_ec_trmm = sum_ec_trmm + ((ec_week_year - ec_week_climatology)-(trmm_week_year - trmm_week_climatology))**2;
               sum_trmm = sum_trmm + (trmm_week_year - trmm_week_climatology)**2;

    #Calculate MSSS
    msss = 1 - sum_ec_trmm/sum_trmm;

    #Call function "plot_figure_cora" to plot MSSS
    plot_figure_msss.plot_figure(msss,ec_lat,ec_lon,model_date[:2],str(i_step+1));
