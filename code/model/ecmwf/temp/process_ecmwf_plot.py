'''
#THERE IS THE OPTION TO PRINT OUT A PARTICULAR WEEK and LOCATION TO CHECK THE VALUES 
This script processes the ECMWF file to produce plots of the below three datasets
Weekly average temperature values for a partiucular set of dates (interimWeekly)
Climotology for each of those weeks (interimClimo)
And weekly anomly values (interimAnom)

'''

import datetime
import numpy as np
import s2sUtilitiesThea as s2s


##----------------------------------SPECIFY-----------------------------------------------------------------

#List of all the start dates for the files (see process ECMWF code for more information)
model_initial_date = ['1013','1017','1020','1024','1027','1031','1103','1107','1110','1114','1117','1121','1124'] # 

# the path to the folder for the ec data
ec_input = '../../workshop1/data/model/ecmwf/temp' # will need to change this path 
ec_output = '../../workshop1/data/model/ecmwf'
#the number of lead times (in weeks) that you are looking at
model_step = 4

#Rest of the dates
initMonth = 11
initDate = [3,7,10,14,17,21,24] 
startYear = 1998
endYear = 2014

#Options:
printData= [0,18,13] # set printData = 0 if nothing to print out, otherwise specify [year, latitude location, longitude location]
plotting = False # will prompt for options to specifiy the year and week you want to plot
saving = False # if true, will save the data so you can look in panoply. 
##--------------------------------PROCESSING-------------------------------
#Creating the ecWeekly file. format is [lead_time, date (based on initdate file), year, lat, lon]

for i_date in range(0,len(model_initial_date)):
        model_date = model_initial_date[i_date]
        cur_ec_filename = 'ECMWF_temp_2016-' + model_date[:2] + '-' + model_date[-2:] + '_weekly.nc'
    #no interpolation needed, just need to make sure they are the right way around (which they are not)
        dataLat, dataLon, dataTime, dataStep, ecdata= s2s.getECMWFweekly(ec_input + '/' + cur_ec_filename)
        if i_date == 0 :        
            # format is model step/forecast week, date, year, latitude, longitude
            ectemp = np.empty([model_step, len(model_initial_date),endYear+1-startYear, len(dataLat), len(dataLon)])
            ecWeekly = np.empty([model_step, len(initDate),endYear+1-startYear, len(dataLat), len(dataLon)])
            ecAnom = np.empty([model_step, len(initDate),endYear+1-startYear,len(dataLat), len(dataLon)])
            # format is model step/forecast week, date, latitude, longitude [ no year]
            ecClimo = np.empty([model_step, len(initDate),len(dataLat), len(dataLon)])
            
        for i_step in range(model_step): 
            ectemp[i_step, i_date, :, :, :] = ecdata[:endYear-startYear+1, i_step, :, :]
    
    #now creating the ecWeekly to be within the bounds
for date in range(len(initDate)):
        if initDate[date] <10:
            model_date = str(initMonth)+str(0)+str(initDate[date])
        else:
            model_date = str(initMonth)+str(initDate[date])

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


if printData !=0 :
        print('Printing values for location : '+ str(dataLat[printData[1]]) +"N "+str(dataLon[printData[2]])+"E")
       
        print("Climatology ")
        print(ecClimo[:,:,printData[1], printData[2]]) 
        
        for i in range(model_step):
            print("Weekly values for lead time " +str(i))
            print(ecWeekly[i,:, printData[0], printData[1], printData[2]]) 
            print("Anomaly values")
            print(ecAnom[i,:,printData[0],  printData[1], printData[2]]) 
##---------------------------------------------------PRINTING--------------------------------------
if plotting: 
    while plotting:
        plotYear = round(float(input('Please enter the year you would like to print: ')))
        while (plotYear < startYear) | (plotYear > endYear):
            plotYear = round(float(input('This year is out of range. Please enter the year you would like to print: ')))
        plotWeek = round(float(input('Please enter the week you would like to print: 0 -'+str(len(initDate)))))
        while (plotWeek < 0) | (plotWeek > len(initDate)):
            plotWeek = round(float(input('This week is out of range. Please enter the week you would like to print: ')))

        for i in range(model_step):
            j = plotWeek
            k = plotYear- startYear
         #Define title and name convention
            title_str = 'Average Temperature, ECMWF HindCast '
            name_str = 'ecmwf_' +"step "+str(i)+'for date ' +str(plotYear)+'-'+str(initMonth) +str(initDate[j])+'_' + 'Average'+'.png'
            s2s.plot_figure(ecWeekly[i,j,k, :, :],dataLat,dataLon,[240,300],title_str,name_str,'Average')
            title_str = 'Temperature Climatology, ECMWF HindCast '
            name_str = 'ecmwf_' +"step "+str(i)+'for date ' +str(plotYear)+'-'+str(initMonth) +str(initDate[j])+'_' + 'Climatology'+'.png'
            s2s.plot_figure(ecClimo[i,j, :, :],dataLat,dataLon,[240,300],title_str,name_str,'Climatology')
            title_str = 'Temperature Anomaly, ECMWF HindCast '
            name_str = 'ecmwf_' +"step "+str(i)+'for date ' +str(plotYear)+'-'+str(initMonth) +str(initDate[j])+'_' + 'Anomaly'+'.png'
            s2s.plot_figure(ecAnom[i,j,k, :, :],dataLat,dataLon,[-3,3],title_str,name_str,'Anomaly')
        plotting = False
        change = input('Would you like to plot more figures? Input Y or N ')
        if (change == 'Y') | (change == 'y') :
            plotting = True
## ------------------------------------------------SAVING-------------------------------------------
if saving:
    ec_filename = 'ECWMF_Month' + str(initMonth) + '_Average_Weekly.nc'
    s2s.write_ec(ec_output,ec_filename,ecWeekly,range(model_step),range(len(initDate)),range(startYear, endYear+1),dataLat,dataLon,'Average')
    ec_filename = 'ECWMF_Month' + str(initMonth) + '_Anomaly_Weekly.nc'
    s2s.write_ec(ec_output,ec_filename,ecAnom,range(model_step),range(len(initDate)),range(startYear, endYear+1),dataLat,dataLon,'Anomaly')
    ec_filename = 'ECWMF_Month' + str(initMonth) + '_Climatology_Weekly.nc'
    s2s.write_ec(ec_output,ec_filename,ecClimo,range(model_step),range(len(initDate)),range(startYear, endYear+1),dataLat,dataLon,'Climatology')