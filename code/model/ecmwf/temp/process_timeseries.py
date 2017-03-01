
import plot_timeseries

import processFunctions as pf
import s2s_utilities_temp as s2s

##-----------------------------------------------------
#		SPECIFY
#------------------------------------------------------
model_initial_date = ['1013','1017','1020','1024','1027','1031','1103','1107','1110','1114','1117','1121','1124'] # this is the name of all the ECMWF files for the start dates
# make sure this list matches with the files you downloaded
weeks = [3,7,10,14,17,21,24] # these are the start dates for the weeks you are looking for. Make sure they match with the model data!
month = 11 # this is the month you want to be looking at 
start_year = 1998 
end_year = 2014 
lead_times = 4 # this is the number of lead time weeks 
ec_input = '../../../../data/model/ecmwf/temp' # will need to change this path 

#the domain
lat_up = 10
lat_down = -10
lon_left = 90
lon_right = 110

target_week  = 0


#--------------------#This part is to prepare ERA-I and ECMWF anomaly data
#---------------------------------------


#get the Interim data (similar to process script)
erai_lon, erai_lat, erai_dates, erai_anom= pf.processInterim(month, weeks, start_year, end_year, 3)
LD, LU, LL, LR, erai_lat, erai_lon = s2s.makeSmaller(erai_lat, erai_lon, lat_up, lat_down, lon_left, lon_right)

#Get the EC and EI data
erai_anom = erai_anom[:,:,LD:LU+1,LL:LR+1]


# get the Hindcast data Anomalies
ec_lon, ec_lat, ec_anom = pf.processEcmwfTemp(ec_input, model_initial_date, lead_times, month, weeks, start_year, end_year, 3)
LD, LU, LL, LR, ec_lat, ec_lon = s2s.makeSmaller(ec_lat, ec_lon, lat_up, lat_down, lon_left, lon_right)

ec_anom = ec_anom[:,:,:,LD:LU+1,LL:LR+1]




#------------------------
#This part is to display time series of anomalies
#---------------


#
title_str = 'Temperature Anomaly Time Series' + '\n' + str(weeks[target_week])+'/11'
name_str = 'ECMWF_Temperature_Timeseries_' + str(weeks[target_week]) + '-' + str(month) + '.png'

plot_timeseries.plot_fig(erai_anom,ec_anom,target_week,start_year,end_year,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,title_str,name_str)