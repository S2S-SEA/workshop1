import numpy
import calendar
from scipy import interpolate
import plot_timeseries

#Initial setup
week_initial_date = ['1103','1107','1110','1114','1117','1121','1124']
target_month = 11
start_year = 1998
end_year = 2014

#---------------------------------------------------
#This part is to prepare TRMM and ECMWF anomaly data
#---------------------------------------------------

#Define TRMM input path
trmm_input = '../../../../data/obs/prec'
trmm_filename = 'TRMM_' + calendar.month_abbr[target_month] + '_Anomaly_Weekly.nc'
cur_trmm_path = trmm_input + '/' + trmm_filename

#Define ECMWF input path
ec_input = '../../../../data/model/ecmwf/prec'
ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_Anomaly_Weekly.nc'
cur_ec_path = ec_input + '/' + ec_filename

#Read TRMM and ECMWF data
trmm_lat,trmm_lon,trmm_anomaly_0 = plot_timeseries.read_anomaly(cur_trmm_path,'TRMM')
ec_lat,ec_lon,ec_anomaly = plot_timeseries.read_anomaly(cur_ec_path,'ECMWF')

#Interpolate TRMM to ECMWF resolution
trmm_anomaly = numpy.empty([trmm_anomaly_0.shape[0],trmm_anomaly_0.shape[1],len(ec_lat),len(ec_lon)])
for i in range(0,trmm_anomaly.shape[0]):
    for j in range(0,trmm_anomaly.shape[1]):
        pi = interpolate.interp2d(trmm_lon,trmm_lat,trmm_anomaly_0[i,j,:,:])
        trmm_anomaly[i,j,:,:] = pi(numpy.asarray(ec_lon),numpy.asarray(ec_lat))

#-----------------------------------------------------
#This part is to display the time series for anomalies
#-----------------------------------------------------

#Define the week for display
target_week = 0    #week number starting from 0

#Define the domain for display
lat_down = -20
lat_up = 30
lon_left = 80
lon_right = 150

#Plot time series
start_date = week_initial_date[target_week]
end_date = "%02d"%target_month + "%02d"%(int(start_date[-2:])+6)
title_str = 'Rainfall Anomaly Time Series' + '\n' + start_date + '-' + end_date
name_str = 'ECMWF_Rainfall_Timeseries_' + start_date + '-' + end_date + '.png'
plot_timeseries.plot_fig(trmm_anomaly,ec_anomaly,target_week,start_year,end_year,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,title_str,name_str)