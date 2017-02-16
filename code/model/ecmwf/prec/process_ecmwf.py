import datetime
import numpy
import netCDF4
import calendar
import s2s_utility_prec

#Initial setup
model_initial_date = ['1013','1017','1020','1024','1027','1031','1103','1107','1110','1114','1117','1121','1124']
week_initial_date = ['1103','1107','1110','1114','1117','1121','1124']
target_month = 11
start_year = 1998
end_year = 2014
model_step = 4

#-------------------------------------------------------------------
#This part is to calculate ECMWF rainfall climatology/average/anomaly
#-------------------------------------------------------------------

#Define ECMWF input path
ec_input = '../../../../data/model/ecmwf/prec'

#Read ECMWF lat/lon
nc = netCDF4.Dataset(ec_input + '/' + 'ECMWF_prec_2016-10-13_weekly.nc')
ec_lat_0 = nc.variables['latitude'][:]
ec_lat = ec_lat_0[::-1]    #reverse lat
ec_lon = nc.variables['longitude'][:]
nc.close()

ec_average = numpy.empty([model_step,len(week_initial_date),end_year-start_year+1,len(ec_lat),len(ec_lon)])    #step,week,year,lat,lon
ec_anomaly = numpy.empty([model_step,len(week_initial_date),end_year-start_year+1,len(ec_lat),len(ec_lon)])

#For each model initial date
for i_date in range(0,len(model_initial_date)):
    model_date = model_initial_date[i_date]

    #Find the corresponding data file
    cur_ec_filename = 'ECMWF_prec_2016-' + model_date[:2] + '-' + model_date[-2:] + '_weekly.nc'
    cur_ec_path = ec_input + '/' + cur_ec_filename

    #Read ECMWF dataset
    ec_time,ec_step,ec_data = s2s_utility_prec.read_ec(cur_ec_path)

    #For each model lead time
    for i_step in range(0,model_step):
        end_date = ec_time[0] + datetime.timedelta(hours=int(ec_step[i_step])-24)
        start_date = end_date - datetime.timedelta(days=6)

        #Check if forecasted week is within the target month
        if start_date.month == target_month and end_date.month == target_month:
           i_week = week_initial_date.index("%02d"%start_date.month + "%02d"%start_date.day)
           ec_average[i_step,i_week,:,:,:] = ec_data[:,i_step,:,:]

ec_climatology = numpy.mean(ec_average,axis=2)
for i_year in range(0,end_year-start_year+1):
    ec_anomaly[:,:,i_year,:,:] = ec_average[:,:,i_year,:,:] - ec_climatology

#-----------------------------------------------------------------------------
#This part is to output and display ECMWF rainfall climatology/average/anomaly
#-----------------------------------------------------------------------------

#Define ECMWF output path
ec_output = '../../../../data/model/ecmwf/prec'

#Choose to output or display data
data_output = True
plot_figure = False

if data_output == True:
   #Output ECMWF climatology/average/anomaly
   ec_step = range(0,model_step)
   ec_week = range(0,len(week_initial_date))
   ec_year = range(start_year,end_year+1)

   ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_Climatology_Weekly.nc'
   s2s_utility_prec.write_ec(ec_output,ec_filename,ec_climatology,ec_step,ec_week,ec_year,ec_lat,ec_lon,'Climatology')

   ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_Average_Weekly.nc'
   s2s_utility_prec.write_ec(ec_output,ec_filename,ec_average,ec_step,ec_week,ec_year,ec_lat,ec_lon,'Average')

   ec_filename = 'ECMWF_' + calendar.month_abbr[target_month] + '_Anomaly_Weekly.nc'
   s2s_utility_prec.write_ec(ec_output,ec_filename,ec_anomaly,ec_step,ec_week,ec_year,ec_lat,ec_lon,'Anomaly')

if plot_figure == True:
   #Define target week and year
   target_week = 6    #week number starting from 0
   target_year = 2014

   #Define the domain for display
   lat_down = -20
   lat_up = 30
   lon_left = 80
   lon_right = 150
   grid_lat = 10
   grid_lon = 10

   #Plot ECMWF climatology/average/anomaly
   for i_step in range(0,model_step):
       start_date = week_initial_date[target_week]
       end_date = "%02d"%target_month + "%02d"%(int(start_date[-2:])+6)

       data_range = [0,18]    #change data range for plotting accordingly
       title_str = 'ECMWF Rainfall Climatology' + '\n' + start_date + '-' + end_date + ' (LT' + str(i_step+1) + ')'
       name_str = 'ECMWF_' + start_date + '-' + end_date + '_' + 'LT' + str(i_step+1) + '_Climatology.png'
       s2s_utility_prec.plot_processing(ec_climatology[i_step,target_week,:,:],ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Climatology')

       data_range = [0,36]
       title_str = 'ECMWF Rainfall Average' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date + ' (LT' + str(i_step+1) + ')'
       name_str = 'ECMWF_' + str(target_year) + '_' + start_date + '-' + end_date + '_' + 'LT' + str(i_step+1) + '_Average.png'
       s2s_utility_prec.plot_processing(ec_average[i_step,target_week,target_year-start_year,:,:],ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Average')

       data_range = [-10,10]
       title_str = 'ECMWF Rainfall Anomaly' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date + ' (LT' + str(i_step+1) + ')'
       name_str = 'ECMWF_' + str(target_year) + '_' + start_date + '-' + end_date + '_' + 'LT' + str(i_step+1) + '_Anomaly.png'
       s2s_utility_prec.plot_processing(ec_anomaly[i_step,target_week,target_year-start_year,:,:],ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Anomaly')
