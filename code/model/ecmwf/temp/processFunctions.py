'''

This function processes the ERA-Interim file to produce plots of the below three datasets
Weekly average temperature values for a partiucular set of dates (interimWeekly)
Climotology for each of those weeks (interimClimo)
And weekly anomly values (interimAnom)
The same method as in the process_interim file.

If the file doesn't run, check the start file and file names are correct. 
'''

import datetime
import numpy as np
import s2s_utilities_temp as s2s
import sys 
import os

def processInterim(month, weeks, startYear, endYear, type):
 #Input: 
 #month ( the single month that you are looking at) e.g. 11
 #weeks : list of the first days in the week that you are looking at e.g. [3,7,10,14,17,21,24] 
 #startYear/endYear : first and last year that you are looking at e.g 1998
 #Returns:
 #lons, lats, dates, erai_Type
 #if type == 1, returns the weekly absolute value, 2 == climatology value, 3 = anomaly
    startfile= "../../../.."
    file = "/data/obs/temp/erai_temp_6hr_"
    file2 = "/data/obs/temp/interim_temp_6hr_"
    filename = startfile+file+str(startYear)+".nc"
    filename2 = startfile+file2+str(startYear)+".nc"
    if os.path.exists(filename):
        print('Found file ' +filename)
    elif os.path.exists(filename2):
        print('Found file ' +filename2)
        file = file2
    else:
        print('Cannot find the ERA-Interim file')
        sys.exit()

##--------------------------------PROCESSING-------------------------------
#Creating the interimWeekly file. format is [year, week (based on weeks file), lat, lon]

    for year in range(startYear, endYear+1):
        filename = startfile+file+str(year)+".nc"
	
        lons, lats, dateList, t2m = s2s.getInterim(filename)
  
        if year == startYear :
            interimWeekly = np.empty([len(weeks),endYear+1-startYear, len(lats), len(lons)])
            dates = []

        count = 0
        for i in weeks:       
            index = int(np.where(dateList == datetime.datetime(year, month, i, 0, 0))[0]) #find the date in the interim data
            interimWeekly[count, year-startYear,:, :] = np.mean(t2m[index:index+7*4, :, :], axis = 0)#average the weekly values (4*7)
            count+= 1
            dates.append(datetime.datetime(year, month, i, 0, 0))
#creating the climatology file (average over all the weeks with same start day)
    interimClimo = np.mean(interimWeekly, axis = 0)


# Creating the weekly temperature anomaly, same format as the interimWeekly file
    interimAnom = np.empty(interimWeekly.shape)
    for i in range(len(weeks)):
        interimAnom[i,:,:,:] = interimWeekly[i, :, :, :] - interimClimo[i, :, :]
    if type == 1:
        interimType = interimWeekly
    elif type == 2:
        interimType = interimClimo
    elif type == 3:
        interimType = interimAnom
    return lons, lats, dates, interimType

def processEcmwfTemp(ec_input, model_initial_date, lead_times ,month, weeks, start_year, end_year, type):
 #Input: 
 # the path to the folder for the ec data
 #a List of all the start dates for the files (see process ECMWF code for more information)
 #the number of lead times (in weeks) that you are looking at
 #month ( the single month that you are looking at) e.g. 11
 #weeks : list of the first days in the week that you are looking at e.g. [3,7,10,14,17,21,24] 
 #startYear/endYear : first and last year that you are looking at e.g 1998
 #if type == 1, returns the weekly absolute value, 2 == climatology value, 3 = anomaly

 # returns ec_lon (longitude file), ec_lat (latitude file), ecType (the data, either weekly, anom, or climatology)
##--------------------------------PROCESSING-------------------------------
#Creating the ecWeekly file. format is [lead_time, date (based on weeks file), year, lat, lon]

    for i_date in range(0,len(model_initial_date)):
        
        model_date = model_initial_date[i_date]
        cur_ec_filename = 'ECMWF_temp_2016-' + model_date[:2] + '-' + model_date[-2:] + '_weekly.nc'
        #loading the previously saved data
        ec_lat, ec_lon, ec_time, ec_step, ec_data= s2s.getECMWFweekly(ec_input + '/' + cur_ec_filename)
        
        if i_date == 0  :
            ec_weekly = np.empty([lead_times, len(weeks),end_year+1-start_year, len(ec_lat), len(ec_lon)])
            ec_anom = np.empty([lead_times, len(weeks),end_year+1-start_year,len(ec_lat), len(ec_lon)])
            ec_clim = np.empty([lead_times, len(weeks),len(ec_lat), len(ec_lon)])

        for i_step in range(0,lead_times):
            end_date = ec_time[0] + datetime.timedelta(hours=int(ec_step[i_step]))
            start_date = end_date - datetime.timedelta(days=6)


        #Check if forecasted week is within the target month
            if start_date.month == month and end_date.month == month:
                try:
                    i_week = weeks.index(start_date.day)
                except:
                    print(i_step)
                    print("The date "+ str(start_date) + " was not found in list of weeks. Check the model inital_date list and week list")
                ec_weekly[i_step,i_week,:,:,:] = ec_data[:end_year+1-start_year,i_step,:,:]


        ec_clim = np.mean(ec_weekly[:, :, :, :, :], axis = 2)
        for i_year in range(0,end_year-start_year+1):
            ec_anom[:,:,i_year,:,:] = ec_weekly[:,:,i_year,:,:] - ec_clim

    if type == 1:
        ecType = ec_weekly
    elif type == 2:
        ecType = ec_clim
    elif type == 3:
        ecType = ec_anom
    return ec_lon, ec_lat, ecType
