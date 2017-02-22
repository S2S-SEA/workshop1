'''
This script calculates CORA for temperature using ERA interim and model data. 
It calls the processInterim and processECMWF files to calculate the weekly anomalies. 
Make sure you check all the conditional files.
Option to print out data or plot data.  

'''
#this is calculating CORA 
import datetime
import numpy as np
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
lat_up = 30
lat_down = -20.5
lon_left = 80
lon_right = 150

#options
print_data=[1,14,14] # set print_data = 0 if nothing to print out, otherwise specify [lead_time location, latitude location, longitude location]
plotting = False# if True, the plots will be done and saved, no plots if False
##-------------------------------------------------------
#			PROCESSING
#---------------------------------------------------------
#check print option
if print_data != 0:
    while print_data[0]>= lead_times:
        print_data[0] = input('Your lead time is out of bounds. Please enter a number between 0 and '+ str(lead_times-1))
    
#get the Interim data (similar to process script)
erai_lon, erai_lat, erai_dates, erai_anom= pf.processInterim(month, weeks, start_year, end_year, 3)
LD, LU, LL, LR, erai_lat, erai_lon = s2s.makeSmaller(erai_lat, erai_lon, lat_up, lat_down, lon_left, lon_right)

erai_anom = erai_anom[:,:,LD:LU+1,LL:LR+1]

if print_data != 0:
	print('Printing values for location '+ str(erai_lat[print_data[1]])+ 'N and ' +str(erai_lon[print_data[2]])+'E')
print("ERA-Interim data starting from " + str(erai_dates[0]) + " to " + str(erai_dates[-1])) 

# get the Hindcast data Anomalies
ec_lon, ec_lat, ec_anom = pf.processEcmwfTemp(ec_input, model_initial_date, lead_times, month, weeks, start_year, end_year, 3)
LD, LU, LL, LR, ec_lat, ec_lon = s2s.makeSmaller(ec_lat, ec_lon, lat_up, lat_down, lon_left, lon_right)
ec_anom = ec_anom[:,:,:,LD:LU+1,LL:LR+1]


# format is model step/forecast week,  latitude, longitude
cora = np.empty([lead_times,len(erai_lat), len(erai_lon)])
msss = np.empty([lead_times,len(erai_lat), len(erai_lon)])

# Now calculating the variables
for i_step in range(lead_times):
        # Getting the variables
        sum_ec_trmm_sq=np.sum(np.sum((ec_anom[i_step, :, :, :, :]-erai_anom[:, :, :, :])**2, axis = 0), axis = 0)
        sum_ec_trmm =np.sum(np.sum(ec_anom[i_step, :, :, :, :]*erai_anom[:, :, :, :], axis = 0), axis = 0)
        sum_ec =  np.sum(np.sum(ec_anom[i_step, :, :, :, :]**2, axis =0), axis = 0)
        sum_trmm =  np.sum(np.sum(erai_anom[:, :, :, :]**2, axis = 0), axis =0)

        #Calculate CORA
        #this is working out the formula = sum(interimAnomaly*ecmwfAnomlay)/(sqrt(sum(interimAnomaly^2))*sqrt(sum(ecmwfAnomaly^2))
        cora[i_step, :, :] = sum_ec_trmm/(sum_ec**(1.0/2)*sum_trmm**(1.0/2))

       #Calculate MSSS 1- MSEh/MSEo for anomalies
        msss[i_step, :, :] = 1 - sum_ec_trmm_sq/sum_trmm


if print_data !=0:
    print('CORA value for the lead time '+str(print_data[0]+1) +' and maximum for all lead times ')
    print(cora[print_data[0], print_data[1],print_data[-1]], np.max(cora[:, print_data[1],print_data[-1]]))
    print('MSSS value for the lead time '+str(print_data[0]+1) +' and maximum for all lead times')
    print(msss[print_data[0], print_data[1],print_data[-1]], np.max(msss[:, print_data[1],print_data[-1]]))

#--------------------------------------------
#			PLOTTING
#--------------------------------------------
## need to add printing option
if plotting: 
    for i_step in range(lead_times):    

        title_str = 'Temperature MSSS' + '\n' + str(month) + ' (LT' + str(i_step+1) + ')'
        name_str = 'ECMWF_' + str(month) + '_LT' + str(i_step+1) + '_MSSS.png'
        s2s.plot_verification(msss[i_step, :, :],ec_lat,ec_lon,10,10,title_str,name_str,'MSSS')
        title_str = 'Temperature CORA' + '\n' + str(month)+ ' (LT' + str(i_step+1) + ')'
        name_str = 'ECMWF_' + str(month) + '_LT' + str(i_step) + '_CORA.png'
        s2s.plot_verification(cora[i_step, :, :],ec_lat,ec_lon,10,10,title_str,name_str,'CORA')