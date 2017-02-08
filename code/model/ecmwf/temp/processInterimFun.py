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
import s2sUtilitiesThea as s2s

##-------------------------------------SPECIFY ----------------------------------------
def processInterim(initMonth, initDate, startYear, endYear, type):
 #Input: 
 #initMonth ( the single month that you are looking at) e.g. 11
 #initDate : list of the first days in the week that you are looking at e.g. [3,7,10,14,17,21,24] 
 #startYear/endYear : first and last year that you are looking at e.g 1998
 #if type == 1, returns the weekly absolute value, 2 == climatology value, 3 = anomaly
    startfile= "../../workshop1"
    file = "/data/obs/temp/interim_temp_6hr_"

##--------------------------------PROCESSING-------------------------------
#Creating the interimWeekly file. format is [year, week (based on initdate file), lat, lon]

    for year in range(startYear, endYear+1):
        filename = startfile+file+str(year)+".nc"
        lons, lats, dateList, t2m = s2s.getInterim(filename)
  
        if year == startYear :
            interimWeekly = np.empty([endYear+1-startYear,len(initDate), len(lats), len(lons)])
            intDate = []

        count = 0
        for i in initDate:       
            index = int(np.where(dateList == datetime.datetime(year, initMonth, i, 0, 0))[0]) #find the date in the interim data
            interimWeekly[year-startYear,count,:, :] = np.mean(t2m[index:index+7*4, :, :], axis = 0)#average the weekly values (4*7)
            count+= 1
            intDate.append(datetime.datetime(year, initMonth, i, 0, 0))
#creating the climatology file (average over all the weeks with same start day)
    interimClimo = np.mean(interimWeekly, axis = 0)


# Creating the weekly temperature anomaly, same format as the interimWeekly file
    interimAnom = np.empty(interimWeekly.shape)
    for i in range(7):
        interimAnom[:,i,:,:] = interimWeekly[:, i, :, :] - interimClimo[i, :, :]
    if type == 1:
        interimType = interimWeekly
    elif type == 2:
        interimType = interimClimo
    elif type == 3:
        interimType = interimAnom
    return lons, lats, intDate, interimType
