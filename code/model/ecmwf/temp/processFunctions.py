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


def processInterim(month, weeks, startYear, endYear, type):
 #Input: 
 #month ( the single month that you are looking at) e.g. 11
 #weeks : list of the first days in the week that you are looking at e.g. [3,7,10,14,17,21,24] 
 #startYear/endYear : first and last year that you are looking at e.g 1998
 #Returns:
 #lons, lats, dates, erai_Type
 #if type == 1, returns the weekly absolute value, 2 == climatology value, 3 = anomaly
    startfile= "../../../.."
    file = "/data/obs/temp/interim_temp_6hr_"

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

def processEcmwfTemp(ec_input, model_initial_date, model_step ,month, weeks, startYear, endYear, type):
 #Input: 
 # the path to the folder for the ec data
 #a List of all the start dates for the files (see process ECMWF code for more information)
 #the number of lead times (in weeks) that you are looking at
 #month ( the single month that you are looking at) e.g. 11
 #weeks : list of the first days in the week that you are looking at e.g. [3,7,10,14,17,21,24] 
 #startYear/endYear : first and last year that you are looking at e.g 1998
 #if type == 1, returns the weekly absolute value, 2 == climatology value, 3 = anomaly

 # returns dataLon (longitude file), dataLat (latitude file), ecType (the data, either weekly, anom, or climatology)
##--------------------------------PROCESSING-------------------------------
#Creating the ecWeekly file. format is [lead_time, date (based on weeks file), year, lat, lon]

    for i_date in range(0,len(model_initial_date)):
        model_date = model_initial_date[i_date]
        cur_ec_filename = 'ECMWF_temp_2016-' + model_date[:2] + '-' + model_date[-2:] + '_weekly.nc'
    #no interpolation needed, just need to make sure they are the right way around (which they are not)
        dataLat, dataLon, dataTime, dataStep, ecdata= s2s.getECMWFweekly(ec_input + '/' + cur_ec_filename)
        if i_date == 0 :        
            # format is model step/forecast week, date, year, latitude, longitude
            ectemp = np.empty([model_step, len(model_initial_date),endYear+1-startYear, len(dataLat), len(dataLon)])
            ecWeekly = np.empty([model_step, len(weeks),endYear+1-startYear, len(dataLat), len(dataLon)])
            ecAnom = np.empty([model_step, len(weeks),endYear+1-startYear,len(dataLat), len(dataLon)])
            # format is model step/forecast week, date, latitude, longitude [ no year]
            ecClimo = np.empty([model_step, len(weeks),len(dataLat), len(dataLon)])
            
        for i_step in range(model_step): 
            ectemp[i_step, i_date, :, :, :] = ecdata[:endYear-startYear+1, i_step, :, :]
    
    #now creating the ecWeekly to be within the bounds
    for date in range(len(weeks)):
        if weeks[date] <10:
            model_date = str(month)+str(0)+str(weeks[date])
        else:
            model_date = str(month)+str(weeks[date])

        if model_date in model_initial_date:
                newdate = model_initial_date.index(model_date)
                i_step = 0
                while newdate>= 0 and i_step<model_step:             
                    ecWeekly[i_step, date, :, :, :] = ectemp[i_step, newdate, :, :, :]
                    ecClimo[i_step,  date, :, :] = np.mean(ectemp[i_step, newdate, :, :, :], axis = 0)
                    ecAnom[i_step,  date, :, :] = ecWeekly[i_step, date,:, :, :] - ecClimo[i_step, date, :, :]
                    i_step += 1
                    newdate -= 1

        else:
            print("The date "+ model_date + " was not found in the ECWMF file. Check the model inital_date list file")
    if type == 1:
        ecType = ecWeekly
    elif type == 2:
        ecType = ecClimo
    elif type == 3:
        ecType = ecAnom
    return dataLon, dataLat, ecType
