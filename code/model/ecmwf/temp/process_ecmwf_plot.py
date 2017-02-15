'''
#THERE IS THE OPTION TO PRINT OUT A PARTICULAR WEEK and LOCATION TO CHECK THE VALUES 
This script processes the ECMWF file to produce plots of the below three datasets
Weekly average temperature values for a partiucular set of dates (interimWeekly)
Climotology for each of those weeks (interimClimo)
And weekly anomly values (interimAnom)

'''

import datetime
import numpy as np
import s2s_utilities_temp as s2s


##----------------------------------SPECIFY-----------------------------------------------------------------

#List of all the start dates for the files (see process ECMWF code for more information)
model_initial_date = ['1013','1017','1020','1024','1027','1031','1103','1107','1110','1114','1117','1121','1124'] # 

# the path to the folder for the ec data
ec_input = '../../../../data/model/ecmwf/temp' # will need to change this path 
ec_output = '../../../../data/model/ecmwf'
#the number of lead times (in weeks) that you are looking at
lead_times = 4

#Rest of the dates
month = 11
weeks = [3,7,10,14,17,21,24] 
start_year = 1998
end_year = 2014

#Options:
print_data= [0,18,13] # set print_data = 0 if nothing to print out, otherwise specify [year, latitude, location, longitude location]
plotting = True # will prompt for options to specifiy the year and week you want to plot
saving = True # if true, will save the data so you can look in panoply. 
##--------------------------------PROCESSING-------------------------------
#Creating the ec_weekly file. Format is [lead_time, date (based on weeks file), year, lat, lon]

for i_date in range(0,len(model_initial_date)):
        
        model_date = model_initial_date[i_date]
        cur_ec_filename = 'ECMWF_temp_2016-' + model_date[:2] + '-' + model_date[-2:] + '_weekly.nc'
        #loading the previously saved data
        ec_lat, ec_lon, ec_time, ec_step, ecdata= s2s.getECMWFweekly(ec_input + '/' + cur_ec_filename)
       
        if i_date == 0 :        
            #creating the empty arrays that we will fill later
            # format is lead time, week, year, latitude, longitude
            ectemp = np.empty([lead_times, len(model_initial_date),end_year+1-start_year, len(ec_lat), len(ec_lon)])
            ec_weekly = np.empty([lead_times, len(weeks),end_year+1-start_year, len(ec_lat), len(ec_lon)])
            ec_anom = np.empty([lead_times, len(weeks),end_year+1-start_year,len(ec_lat), len(ec_lon)])
            ec_clim = np.empty([lead_times, len(weeks),len(ec_lat), len(ec_lon)])
        
         #puting the ecdata in the same format as  above  
        for i_step in range(lead_times): 
            ectemp[i_step, i_date, :, :, :] = ecdata[:end_year-start_year+1, i_step, :, :]
    
    #now creating the ec_weekly to only contain the values within the correct weeks
for date in range(len(weeks)):

        if weeks[date] <10:
            model_date = str(month)+str(0)+str(weeks[date])
        else:
            model_date = str(month)+str(weeks[date])

        if model_date in model_initial_date:
                newdate = model_initial_date.index(model_date)
                i_step = 0

                #populating the three files
                while newdate>= 0 and i_step<lead_times:             
                    ec_weekly[i_step, date, :, :, :] = ectemp[i_step, newdate, :, :, :]
                    ec_clim[i_step,  date, :, :] = np.mean(ectemp[i_step, newdate, :, :, :], axis = 0)
                    ec_anom[i_step,  date, :, :] = ec_weekly[i_step, date,:, :, :] - ec_clim[i_step, date, :, :]
                    i_step += 1
                    newdate -= 1

        else:
            print("The date "+ model_date + " was not found in the ECWMF file. Check the model inital_date list file")

# just some information to print out
if print_data !=0 :
        print('Printing values for location : '+ str(ec_lat[print_data[1]]) +"N "+str(ec_lon[print_data[2]])+"E")
        print("Climatology ")
        print(ec_clim[:,:,print_data[1], print_data[2]]) 
        
        for i in range(lead_times):
            print("Weekly values for lead time " +str(i))
            print(ec_weekly[i,:, print_data[0], print_data[1], print_data[2]]) 
            print("Anomaly values")
            print(ec_anom[i,:,print_data[0],  print_data[1], print_data[2]]) 
##---------------------------------------------------PLOTTING-------------------------------------
# if set to True, this will make some plots for a particular year and week (all climatology, average temp and anomaly will print out). 
if plotting: 
    while plotting:
        plot_year = round(float(input('Please enter the year you would like to print: ')))
        while (plot_year < start_year) | (plot_year > end_year):
            plot_year = round(float(input('This year is out of range. Please enter the year you would like to print: ')))
        plot_week = round(float(input('Please enter the week you would like to print: 0 -'+str(len(weeks)))))
        while (plot_week < 0) | (plot_week > len(weeks)):
            plot_week = round(float(input('This week is out of range. Please enter the week you would like to print: ')))

        for i in range(lead_times):
            j = plot_week
            k = plot_year- start_year

         #Define title and name convention
            title_str = 'Average Temperature, ECMWF HindCast '
            name_str = 'ecmwf_' +"step "+str(i)+'for date ' +str(plot_year)+'-'+str(month) +str(weeks[j])+'_' + 'Average'+'.png'
            s2s.plot_figure(ec_weekly[i,j,k, :, :],ec_lat,ec_lon,[240,300],title_str,name_str,'Average')
            title_str = 'Temperature Climatology, ECMWF HindCast '
            name_str = 'ecmwf_' +"step "+str(i)+'for date ' +str(plot_year)+'-'+str(month) +str(weeks[j])+'_' + 'Climatology'+'.png'
            s2s.plot_figure(ec_clim[i,j, :, :],ec_lat,ec_lon,[240,300],title_str,name_str,'Climatology')
            title_str = 'Temperature Anomaly, ECMWF HindCast '
            name_str = 'ecmwf_' +"step "+str(i)+'for date ' +str(plot_year)+'-'+str(month) +str(weeks[j])+'_' + 'Anomaly'+'.png'
            s2s.plot_figure(ec_anom[i,j,k, :, :],ec_lat,ec_lon,[-3,3],title_str,name_str,'Anomaly')
        plotting = False
        change = input('Would you like to plot more figures? Input Y or N ')
        if (change == 'Y') | (change == 'y') :
            plotting = True
## ------------------------------------------------SAVING-------------------------------------------
#if set to True, this will save the data so you can plot it in panoply or use it later. 
if saving:
    ec_filename = 'ECWMF_Month' + str(month) + '_Average_Weekly.nc'
    s2s.write_ec(ec_output,ec_filename,ec_weekly,range(lead_times),range(len(weeks)),range(start_year, end_year+1),ec_lat,ec_lon,'Average')
    ec_filename = 'ECWMF_Month' + str(month) + '_Anomaly_Weekly.nc'
    s2s.write_ec(ec_output,ec_filename,ec_anom,range(lead_times),range(len(weeks)),range(start_year, end_year+1),ec_lat,ec_lon,'Anomaly')
    ec_filename = 'ECWMF_Month' + str(month) + '_Climatology_Weekly.nc'
    s2s.write_ec(ec_output,ec_filename,ec_clim,range(lead_times),range(len(weeks)),range(start_year, end_year+1),ec_lat,ec_lon,'Climatology')