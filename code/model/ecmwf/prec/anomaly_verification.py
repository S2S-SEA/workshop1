import numpy
import calendar
from scipy import interpolate
import s2s_utility

#Initial setup
target_month = 11
cora_processing = True
msss_processing = False

#---------------------------------------------------
#This part is to prepare TRMM and ECMWF anomaly data
#---------------------------------------------------

#Define TRMM input path
trmm_input = '.../data/obs/prec'
trmm_filename = 'TRMM_Nov_Anomaly_Weekly.nc'
cur_trmm_path = trmm_input + '/' + trmm_filename

#Define ECMWF input path
ec_input = '.../data/model/ecmwf/prec'
ec_filename = 'ECMWF_Nov_Anomaly_Weekly.nc'
cur_ec_path = ec_input + '/' + ec_filename

#Read TRMM and ECMWF data
trmm_lat,trmm_lon,trmm_anomaly_0 = s2s_utility.read_anomaly(cur_trmm_path,'TRMM')
ec_lat,ec_lon,ec_anomaly = s2s_utility.read_anomaly(cur_ec_path,'ECMWF')

#Interpolate TRMM to ECMWF resolution
trmm_anomaly = numpy.empty([trmm_anomaly_0.shape[0],trmm_anomaly_0.shape[1],len(ec_lat),len(ec_lon)])
for i in range(0,trmm_anomaly.shape[0]):
    for j in range(0,trmm_anomaly.shape[1]):
        pi = interpolate.interp2d(trmm_lon,trmm_lat,trmm_anomaly_0[i,j,:,:])
        trmm_anomaly[i,j,:,:] = pi(numpy.asarray(ec_lon),numpy.asarray(ec_lat))

#-----------------------------------------------
#This part is to calculate and display CORA/MSSS
#-----------------------------------------------

#Define the domain for display
lat_down = -20
lat_up = 30
lon_left = 80
lon_right = 150
grid_lat = 10
grid_lon = 10

if cora_processing == True:
   #For each model lead time
   for i_step in range(0,ec_anomaly.shape[0]):
       sum_ec_trmm = numpy.zeros([len(ec_lat),len(ec_lon)])
       sum_ec = numpy.zeros([len(ec_lat),len(ec_lon)])
       sum_trmm = numpy.zeros([len(ec_lat),len(ec_lon)])

       #For each week
       for i_week in range(0,ec_anomaly.shape[1]):
           #For each year
           for i_year in range(0,ec_anomaly.shape[2]):
               sum_ec_trmm = sum_ec_trmm + ec_anomaly[i_step,i_week,i_year,:,:]*trmm_anomaly[i_week,i_year,:,:]
               sum_ec = sum_ec + ec_anomaly[i_step,i_week,i_year,:,:]**2
               sum_trmm = sum_trmm + trmm_anomaly[i_week,i_year,:,:]**2
       cora = sum_ec_trmm/(sum_ec**(1.0/2)*sum_trmm**(1.0/2))

       #Plot CORA
       title_str = 'Rainfall CORA' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ')'
       name_str = 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_CORA.png'
       s2s_utility.plot_verification(cora,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'CORA')

if msss_processing == True:
   #For each model lead time
   for i_step in range(0,ec_anomaly.shape[0]):
       sum_ec_trmm = numpy.zeros([len(ec_lat),len(ec_lon)])
       sum_trmm = numpy.zeros([len(ec_lat),len(ec_lon)])

       #For each week
       for i_week in range(0,ec_anomaly.shape[1]):
           #For each year
           for i_year in range(0,ec_anomaly.shape[2]):
               sum_ec_trmm = sum_ec_trmm + (ec_anomaly[i_step,i_week,i_year,:,:]-trmm_anomaly[i_week,i_year,:,:])**2
               sum_trmm = sum_trmm + trmm_anomaly[i_week,i_year,:,:]**2
       msss = 1 - sum_ec_trmm/sum_trmm

       #Plot MSSS
       title_str = 'Rainfall MSSS' + '\n' + calendar.month_abbr[target_month] + ' (LT' + str(i_step+1) + ')'
       name_str = 'ECMWF_' + calendar.month_abbr[target_month] + '_LT' + str(i_step+1) + '_MSSS.png'
       s2s_utility.plot_verification(msss,ec_lat,ec_lon,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,'MSSS')
