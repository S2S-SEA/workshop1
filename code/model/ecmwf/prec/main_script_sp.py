'''
This main script processes the downloaded ECMWF dataset to generate weekly climatology, average and anomaly. 
For calculating climatology, average and anomaly for the specified 1 week 11-24 to 11-30,
we take 4 model initial dates 11-03, 11-10, 11-17 and 11-24, and consider forecast week 4, 3, 2 and 1.
This specified  1 week is for demonstration purposes, you can change to other weeks.
For calculating average and anomaly regarding to each individual year,
we take the year of 2014 as an example for demonstration purposes. This is corresponding to previous TRMM data processing.
Self-defined functions "read_ecmwf" and "plot_figure_sp" are used to read ECMWF dataset and for final visualization.
'''

import datetime
import numpy as np
import read_ecmwf
import plot_figure_sp

#Model initial dates, years and steps
model_initial_date = ['1103','1110','1117','1124'];
start_year = 1998;
end_year = 2014;
model_step = 4;

#Target week and year for calculating average and anomaly
target_start_date = '1124';
target_end_date = '1130';
target_year = '2014';

#Specify the domain
lat_up = 30;
lat_down = -20;
lon_left = 80;
lon_right = 150;

#Define ECMWF data path
ec_input = '.../data/model/ecmwf/prec';

#For each model initial date
for i_date in range(0,len(model_initial_date)):
    model_date = model_initial_date[i_date];

    #Find the corresponding data file for each initial date
    cur_ec_filename = 'ECMWF_prec_2016-' + model_date[:2] + '-' + model_date[-2:] + '_weekly.nc'
    cur_ec_path = ec_input + '/' + cur_ec_filename;

    #Call function "read_ecmwf" to read ECMWF dataset and return time, step, latitude, longitude and rainfall values
    ec_time,ec_step,ec_lat,ec_lon,ec_data = read_ecmwf.read_ec(cur_ec_path,lat_up,lat_down,lon_left,lon_right);

    #Calculate python datetime for future date to find corresponding time index
    for i_step in range(0,model_step):
        ec_week_all = np.zeros([len(ec_lat),len(ec_lon)]);
        index = 0;
        for i_year in range(start_year,end_year+1):
            pre_date = ec_time[i_year-start_year] + datetime.timedelta(hours=int(ec_step[i_step])-24);

            #Find corresponding data
            if "%02d"%pre_date.month+"%02d"%pre_date.day == target_end_date:
               ec_week_all = ec_week_all + ec_data[i_year-start_year,i_step,:,:];
               index = index + 1;

        #Calculate weekly climatology
        if index != 0:
           ec_week_climatology = ec_week_all/index;

           #Call function "plot_figure_sp" to plot weekly climatology
           plot_figure_sp.plot_figure(ec_week_climatology,ec_lat,ec_lon,target_start_date,target_end_date,model_date[:2],'none',str(i_step+1),'climatology');

        #Calculate python datetime for future date to find corresponding time index
        for i_year in range(start_year,end_year+1):
            pre_date = ec_time[i_year-start_year] + datetime.timedelta(hours=int(ec_step[i_step])-24);

            #Find corresponding data for weekly average
            if "%04d"%pre_date.year+"%02d"%pre_date.month+"%02d"%pre_date.day == target_year + target_end_date:
               ec_week_year = ec_data[i_year-start_year,i_step,:,:];

               #Calculate weekly anomaly
               ec_week_anomaly = ec_week_year - ec_week_climatology;

               #Call function "plot_figure_sp" to plot weekly average and anomaly
               plot_figure_sp.plot_figure(ec_week_year,ec_lat,ec_lon,target_start_date,target_end_date,model_date[:2],target_year,str(i_step+1),'average');
               plot_figure_sp.plot_figure(ec_week_anomaly,ec_lat,ec_lon,target_start_date,target_end_date,model_date[:2],target_year,str(i_step+1),'anomaly');
