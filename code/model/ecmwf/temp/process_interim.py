'''
#THERE IS THE OPTION TO PRINT OUT A PARTICULAR WEEK and LOCATION TO CHECK THE VALUES 
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

#Options:
printData=[0,18,13] # set printData = 0 if nothing to print out, otherwise specify [year, latitude location, longitude location]
plotting = False# if true, the plots will be done and saved, no plots if false. Check the naming convention is correct under plotting section.
saving = True # If true, will save the date. Check the naming convention is correct under saving section.
outputfile= "../../workshop1/data/obs/" #this is the file to save to. No need to change in saving = False

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
        print('Printing values for location : '+ str(lats[printData[1]]) +"N  "+str(lons[printData[2]])+"E")



#creating the climatology file (average over all the weeks with same start day)
interimClimo = np.mean(interimWeekly, axis = 0)

if printData != 0 : # printing out the value for a specific location 
        print("Climatology ")
        print(interimClimo[:, printData[1], printData[2]]) 

# Creating the weekly temperature anomaly, same format as the interimWeekly file
interimAnom = np.empty(interimWeekly.shape)

for i in range(len(initDate)):
    interimAnom[:,i,:,:] = interimWeekly[:, i, :, :] - interimClimo[i, :, :]

    if printData != 0 : 
        while (printData[0] < startYear) | (printData[0] > endYear) :
            printData[0] = round(float(input('This year is out of range. Please enter the year you would like to print: ') ))
        j = printData[0] - startYear
        print(str(printData[0]) +" Temperature anomaly for week " + str(i))
        print(interimAnom[j, i, printData[1], printData[2]]) 
        print(str(printData[0]) +" Average Temperature for week " + str(i))  
        print(interimWeekly[j, i, printData[1], printData[2]]) 
##---------------------------------------PLOTTING-------------------------------------------
if plotting: 
    plotYear = round(float(input('Please enter the year you would like to print: ')))
    while (plotYear < startYear) | (plotYear > endYear):
        plotYear = input('This year is out of range. Please enter the year you would like to print: ')

    for i in range(len(initDate)):
        j = plotYear- startYear
         #Define title and name convention
        title_str = 'Average Temperature, ERA Interim '
        name_str = 'interim_' +"11-03_11_"+str(initDate[i])+'_' + 'Average'+'.png'
        s2s.plot_figure(interimWeekly[j,i, :, :],lats,lons,[240,300],title_str,name_str,'Average')
        title_str = 'Temperature Climatology, ERA Interim '
        name_str = 'interim_' +"11-03_11_"+str(initDate[i])+'_' + 'Climatology'+'.png'
        s2s.plot_figure(interimClimo[i, :, :],lats,lons,[240,300],title_str,name_str,'Climatology')
        title_str = 'Temperature Anomaly, ERA Interim '
        name_str = 'interim_' +"11-03_11_"+str(initDate[i])+'_' + 'Anomaly'+'.png'
        s2s.plot_figure(interimAnom[j,i, :, :],lats,lons,[-3,3],title_str,name_str,'Anomaly')

##--------------------------------------SAVING-------------------------------------------------
if saving:
# here we save the data to the specified location outputfile, with the name int_filename)
    int_filename = 'ERAInt_Month' + str(initMonth) + '_Anomaly_Weekly.nc'
    s2s.writeInterim(outputfile,int_filename,interimAnom,range(0,len(initDate)),range(startYear,endYear+1),lats,lons,'Anomaly')
    int_filename = 'ERAInt_Month' + str(initMonth) + '_Average_Weekly.nc'
    s2s.writeInterim(outputfile,int_filename,interimWeekly,range(0,len(initDate)),range(startYear,endYear+1),lats,lons,'Average')
    int_filename = 'ERAInt_Month' + str(initMonth) + '_Climatology_Weekly.nc'
    s2s.writeInterim(outputfile,int_filename,interimClimo,range(0,len(initDate)),range(startYear,endYear+1),lats,lons,'Climatology')