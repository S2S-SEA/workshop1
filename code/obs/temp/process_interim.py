﻿'''
#THERE IS THE OPTION TO PRINT OUT A PARTICULAR WEEK and LOCATION TO CHECK THE VALUES 
# MAYBE WANT TO ADD SAVE FUNCTION ? CHECK THE DATA?
This script processes the ERA-Interim file to produce plots of the below three datasets
Weekly average temperature values for a partiucular set of dates (interimWeekly)
Climotology for each of those weeks (interimClimo)
And weekly anomly values (interimAnom)

'''

import datetime
import numpy as np
import s2sUtilitiesThea as s2s

##-------------------------------------SPECIFY ----------------------------------------
# This specifies the location of the files. Note that it assumes that the name of the file, the year is at the end. 
# If not, change lines 17 (& possibly 28) 
startfile= "../../workshop1"
file = "/data/obs/temp/interim_temp_6hr_"

#This contains the information on the date (month, days of the start of each week in the month, and year span)
initMonth = 11 #the month that you are looking at 
initDate = [3,7,10,14,17,21,24] #the start days for each of the weeks
startYear = 1998   
endYear = 2014
printData=[0,18,13] # set printData = 0 if nothing to print out, otherwise specify [week, latitude location, longitude location]
plotting = False# if true, the plots will be done and saved, no plots if false
##--------------------------------PROCESSING-------------------------------
#Creating the interimWeekly file. format is [year, week (based on initdate file), lat, lon]

for year in range(startYear, endYear+1):
    filename = startfile+file+str(year)+".nc"
    print("Loading file "+filename)
    lons, lats, dateList, st = s2s.getInterim(filename)
  
    if year == startYear :
        interimWeekly = np.empty([endYear+1-startYear,len(initDate), len(lats), len(lons)])

    count = 0
    for i in initDate:       
        index = int(np.where(dateList == datetime.datetime(year, initMonth, i, 0, 0))[0]) #find the date in the interim data
        interimWeekly[year-startYear,count,:, :] = np.mean(st[index:index+7*4, :, :], axis = 0)#average the weekly values (4*7)
        count+= 1
    if print !=0 and year == startYear:
        print('Printing values for location : '+ str(lats[printData[1]]) +" "+str(lons[printData[2]]))
    if printData != 0 : # printing out the value for a specific location 
        print("Weekly average value for obs week "+ str(printData[0]))
        print(interimWeekly[year-startYear, printData[0], printData[1], printData[2]]) 

#creating the climatology file (average over all the weeks with same start day)
interimClimo = np.mean(interimWeekly, axis = 0)
if printData != 0 : # printing out the value for a specific location 
        print("Climatology for obs week starting: "+str(printData[0]))
        print(interimClimo[printData[0], printData[1], printData[2]]) 

# Creating the weekly temperature anomaly, same format as the interimWeekly file
interimAnom = np.empty(interimWeekly.shape)
for i in range(7):
    interimAnom[:,i,:,:] = interimWeekly[:, i, :, :] - interimClimo[i, :, :]
    if printData != 0 : 
        print("2014 Temperature anomaly for week " + str(i))
        print(interimAnom[-1, i, printData[1], printData[2]]) 
##---------------------------------------PLOTTING-------------------------------------------
if plotting: 
    for i in range(len(initDate)):
        s2s.plot_figure(interimWeekly[-1,i, :, :],lats,lons,"11-03_11_"+str(initDate[i]),[240,300],'Average')
        s2s.plot_figure(interimClimo[i, :, :],lats,lons,"11-03_11_"+str(initDate[i]),[240,300],'Climatology')
        s2s.plot_figure(interimAnom[-1,i, :, :],lats,lons,"11-03_11_"+str(initDate[i]),[-3,3],'Anomaly')