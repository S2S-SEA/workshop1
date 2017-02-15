import datetime
import numpy
import netCDF4
import calendar
import s2s_utility_prec

#Initial setup
week_initial_date = ['1103','1107','1110','1114','1117','1121','1124']
start_year = 1998
end_year = 2014

#------------------------------------------------------------------
#This part is to calculate TRMM rainfall climatology/average/anomaly
#------------------------------------------------------------------

#Define TRMM input path
trmm_input = '.../data/obs/prec'
trmm_filename = 'TRMM_Daily_Nov_1998-2014.nc'
cur_trmm_path = trmm_input + '/' + trmm_filename

#Read TRMM dataset
trmm_time,trmm_lat,trmm_lon,trmm_data = s2s_utility_prec.read_trmm(cur_trmm_path)

trmm_average = numpy.empty([len(week_initial_date),end_year-start_year+1,len(trmm_lat),len(trmm_lon)])    #week,year,lat,lon
trmm_anomaly = numpy.empty([len(week_initial_date),end_year-start_year+1,len(trmm_lat),len(trmm_lon)])

#For each week initial date
for i_date in range(0,len(week_initial_date)):
    week_date = week_initial_date[i_date]

    #For each year
    for i_year in range(0,end_year-start_year+1):
        cur_date = datetime.datetime(i_year+start_year,int(week_date[:2]),int(week_date[-2:]),12)
        time_index = trmm_time.index(cur_date)

        #Calculate average
        trmm_average[i_date,i_year,:,:] = numpy.mean(trmm_data[time_index:time_index+7,:,:],axis=0)

trmm_climatology = numpy.mean(trmm_average,axis=1)
for i_year in range(0,end_year-start_year+1):
    trmm_anomaly[:,i_year,:,:] = trmm_average[:,i_year,:,:] - trmm_climatology

#-----------------------------------------------------------------------------
#This part is to output and display ECMWF rainfall climatology/average/anomaly
#-----------------------------------------------------------------------------

#Define TRMM output path
trmm_output = '.../data/obs/prec'

#Choose to output or display data
data_output = True
plot_figure = False

if data_output == True:
   #Output TRMM climatology/average/anomaly
   trmm_week = range(0,len(week_initial_date))
   trmm_year = range(start_year,end_year+1)

   trmm_filename = 'TRMM_' + calendar.month_abbr[int(week_date[:2])] + '_Climatology_Weekly.nc'
   s2s_utility_prec.write_trmm(trmm_output,trmm_filename,trmm_climatology,trmm_week,trmm_year,trmm_lat,trmm_lon,'Climatology')

   trmm_filename = 'TRMM_' + calendar.month_abbr[int(week_date[:2])] + '_Average_Weekly.nc'
   s2s_utility_prec.write_trmm(trmm_output,trmm_filename,trmm_average,trmm_week,trmm_year,trmm_lat,trmm_lon,'Average')

   trmm_filename = 'TRMM_' + calendar.month_abbr[int(week_date[:2])] + '_Anomaly_Weekly.nc'
   s2s_utility_prec.write_trmm(trmm_output,trmm_filename,trmm_anomaly,trmm_week,trmm_year,trmm_lat,trmm_lon,'Anomaly')

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

   #Plot TRMM climatology/average/anomaly
   start_date = week_initial_date[target_week]
   end_date = start_date[:2] + "%02d"%(int(start_date[-2:])+6)

   data_range = [0,18]    #change data range for plotting accordingly
   title_str = 'TRMM Rainfall Climatology' + '\n' + start_date + '-' + end_date
   name_str = 'TRMM_' + start_date + '-' + end_date + '_Climatology.png'
   s2s_utility_prec.plot_processing(trmm_climatology[target_week,:,:],trmm_lat,trmm_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Climatology')

   data_range = [0,36]
   title_str = 'TRMM Rainfall Average' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date
   name_str = 'TRMM_' + str(target_year) + '_' + start_date + '-' + end_date + '_Average.png'
   s2s_utility_prec.plot_processing(trmm_average[target_week,target_year-start_year,:,:],trmm_lat,trmm_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Average')

   data_range = [-10,10]
   title_str = 'TRMM Rainfall Anomaly' + '\n' + str(target_year) + ' ' + start_date + '-' + end_date
   name_str = 'TRMM_' + str(target_year) + '_' + start_date + '-' + end_date + '_Anomaly.png'
   s2s_utility_prec.plot_processing(trmm_anomaly[target_week,target_year-start_year,:,:],trmm_lat,trmm_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,'Anomaly')
