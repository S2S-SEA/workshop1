'''
This main script processes the downloaded TRMM dataset to generate weekly climatology, average and anomaly. 
For calculating climatology, average and anomaly for the 7-week periods (please refer to the Excel Sheet),
we take model initial dates from 3rd Nov onwards, and only consider forecast week 1.
For calculating average and anomaly regarding to each individual year,
we take the year of 2014 as an example for demonstration purposes.
Self-defined functions "read_trmm" and "plot_figure_sp" are used to read TRMM dataset and for final visualization.
'''

import datetime
import numpy as np
import read_trmm
import plot_figure_sp

#Model initial dates and years for the 7-week periods
model_initial_date = ['1103','1107','1110','1114','1117','1121','1124'];
start_year = 1998;
end_year = 2014;

#Forecast week 1
start_day = 0;
end_day = 6;

#Target year for calculating average and anomaly
target_year = '2014';

#Specify the domain
lat_up = 30;
lat_down = -20;
lon_left = 80;
lon_right = 150;

#Define TRMM data path
trmm_input = '.../data/obs/prec';
trmm_filename = 'TRMM_Daily_Nov_1998-2014.nc';
cur_trmm_path = trmm_input + '/' + trmm_filename;

#Call function "read_trmm" to read TRMM dataset and return time, latitude, longitude and rainfall values
trmm_time,trmm_lat,trmm_lon,trmm_data = read_trmm.read_trmm(cur_trmm_path,lat_up,lat_down,lon_left,lon_right);

#For each model initial date
for i_date in range(0,len(model_initial_date)):
    model_date = model_initial_date[i_date];
    start_date = model_date;
    end_date = model_date[:2] + "%02d"%(int(model_date[-2:])+6);

    #Calculate python datetime for initial date
    trmm_week_all = np.zeros([len(trmm_lat),len(trmm_lon)]);
    index = 0;
    for i_year in range(start_year,end_year+1):
        cur_year = "%04d"%i_year;
        cur_date = datetime.datetime(int(cur_year),int(model_date[:2]),int(model_date[-2:]));

        #Calculate python datetime for future date to find corresponding time index for reading corresponding data
        trmm_day_all = np.zeros([len(trmm_lat),len(trmm_lon)]);
        for i_day in range(start_day,end_day+1):
            pre_date = cur_date + datetime.timedelta(days=i_day);
            time_index = trmm_time.index("%04d"%pre_date.year + "%02d"%pre_date.month + "%02d"%pre_date.day);

            #Calculate weekly climatology
            trmm_day_all = trmm_day_all + trmm_data[time_index,:,:]
        trmm_week_year = trmm_day_all/7;
        trmm_week_all = trmm_week_all + trmm_week_year;
        index = index + 1;
    trmm_week_climatology = trmm_week_all/index;

    #Call function "plot_figure_sp" to plot weekly climatology
    plot_figure_sp.plot_figure(trmm_week_climatology,trmm_lat,trmm_lon,start_date,end_date,model_date[:2],'none','climatology');

    #Calculate python datetime for current initial date
    cur_year = target_year;
    cur_date = datetime.datetime(int(cur_year),int(model_date[:2]),int(model_date[-2:]));
    trmm_day_all = np.zeros([len(trmm_lat),len(trmm_lon)]);

    #Calculate python datetime for future date to find corresponding time index for reading corresponding data
    for i_day in range(start_day,end_day+1):
        pre_date = cur_date + datetime.timedelta(days=i_day);
        time_index = trmm_time.index("%04d"%pre_date.year + "%02d"%pre_date.month + "%02d"%pre_date.day);

        #Calculate weekly average and anomaly
        trmm_day_all = trmm_day_all + trmm_data[time_index,:,:];
    trmm_week_year = trmm_day_all/7;
    trmm_week_anomaly = trmm_week_year - trmm_week_climatology;

    #Call function "plot_figure_sp" to plot weekly average and anomaly
    plot_figure_sp.plot_figure(trmm_week_year,trmm_lat,trmm_lon,start_date,end_date,model_date[:2],cur_year,'average');
    plot_figure_sp.plot_figure(trmm_week_anomaly,trmm_lat,trmm_lon,start_date,end_date,model_date[:2],cur_year,'anomaly');

