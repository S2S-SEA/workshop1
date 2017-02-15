'''
This script processes the ERA-Interim file to produce plots of the below three datasets
Weekly average temperature values for a partiucular set of dates (erai_weekly)
Climotology for each of those weeks (erai_clim)
And weekly anomly values (erai_anom)
Options include whether to display data on the screen (print_data), to save the data (saving), 
or to plot the data for a particular year (plotting)
'''

import datetime
import numpy as np
import s2s_utilities_temp as s2s

##-------------------------------------SPECIFY ----------------------------------------
# This specifies the location of the files. Note that it assumes that the name of the file, the year is at the end. 
# If not, change lines 17 (& possibly 28) 
start_file= "../../.."
file = "/data/obs/temp/interim_temp_6hr_"

#This contains the information on the date (month, days of the start of each week in the month, and year span)
month = 11 #the month that you are looking at 
weeks = [3,7,10,14,17,21,24] #the start days for each of the weeks
start_year = 1998   
end_year = 2014

#Options:
print_data=0#[0,18,13] # set print_data = 0 if nothing to print out, otherwise specify [year, latitude location, longitude location]
plotting = True# if true, the plots will be done and saved, no plots if false. Check the naming convention is correct under plotting section.
saving = False # If true, will save the date. Check the naming convention is correct under saving section.
output_file= "../../../data/obs/" #this is the file to save to the data to

##--------------------------------PROCESSING-------------------------------
#Creating the erai_weekly file. format is [year, week (based on weeks file), lat, lon]

for year in range(start_year, end_year+1):
    filename = start_file+file+str(year)+".nc"
    print("Loading file "+filename)
    lons, lats, date_list, st = s2s.getInterim(filename)
  
    if year == start_year :
        erai_weekly = np.empty([end_year+1-start_year,len(weeks), len(lats), len(lons)])

    count = 0
    for i in weeks:       
        index = int(np.where(date_list == datetime.datetime(year, month, i, 0, 0))[0]) #find the date in the interim data
        erai_weekly[year-start_year,count,:, :] = np.mean(st[index:index+7*4, :, :], axis = 0)#average the weekly values (4*7)
        count+= 1

    if print_data !=0 and year == start_year:
        print('Printing values for location : '+ str(lats[print_data[1]]) +"N  "+str(lons[print_data[2]])+"E")



#creating the climatology file (average over all the weeks with same start day)
erai_clim = np.mean(erai_weekly, axis = 0)

if print_data != 0 : # printing out the value for a specific location 
        print("Climatology ")
        print(erai_clim[:, print_data[1], print_data[2]]) 

# Creating the weekly temperature anomaly, same format as the erai_weekly file
erai_anom = np.empty(erai_weekly.shape)

for i in range(len(weeks)):
    erai_anom[:,i,:,:] = erai_weekly[:, i, :, :] - erai_clim[i, :, :]

    if print_data != 0 : 
        while (print_data[0] < start_year) | (print_data[0] > end_year) :
            print_data[0] = round(float(input('This year is out of range. Please enter the year you would like to print: ') ))
        j = print_data[0] - start_year
        print(str(print_data[0]) +" Temperature anomaly for week " + str(i))
        print(erai_anom[j, i, print_data[1], print_data[2]]) 
        print(str(print_data[0]) +" Average Temperature for week " + str(i))  
        print(erai_weekly[j, i, print_data[1], print_data[2]]) 
##---------------------------------------PLOTTING-------------------------------------------
if plotting: 
    plotYear = round(float(input('Please enter the year you would like to plot: ')))
    while (plotYear < start_year) | (plotYear > end_year):
        plotYear = input('This year is out of range. Please enter the year you would like to print: ')

    for i in range(len(weeks)):
        j = plotYear- start_year
         #Define title and name convention
        title_str = 'Average Temperature, ERA Interim '
        name_str = 'interim_' +str(plotYear)+"_11_"+str(weeks[i])+'_' + 'Average'+'.png'
        s2s.plot_figure(erai_weekly[j,i, :, :],lats,lons,[240,300],title_str,name_str,'Average')
        title_str = 'Temperature Climatology, ERA Interim '
        name_str = 'interim_' +str(plotYear)+"_11_"+str(weeks[i])+'_' + 'Climatology'+'.png'
        s2s.plot_figure(erai_clim[i, :, :],lats,lons,[240,300],title_str,name_str,'Climatology')
        title_str = 'Temperature Anomaly, ERA Interim '
        name_str = 'interim_' +str(plotYear)+"_11_"+str(weeks[i])+'_' + 'Anomaly'+'.png'
        s2s.plot_figure(erai_anom[j,i, :, :],lats,lons,[-3,3],title_str,name_str,'Anomaly')

##--------------------------------------SAVING-------------------------------------------------
if saving:
# here we save the data to the specified location output_file, with the name int_filename)
    int_filename = 'ERAInt_Month' + str(month) + '_Anomaly_Weekly.nc'
    s2s.writeInterim(output_file,int_filename,erai_anom,range(0,len(weeks)),range(start_year,end_year+1),lats,lons,'Anomaly')
    int_filename = 'ERAInt_Month' + str(month) + '_Average_Weekly.nc'
    s2s.writeInterim(output_file,int_filename,erai_weekly,range(0,len(weeks)),range(start_year,end_year+1),lats,lons,'Average')
    int_filename = 'ERAInt_Month' + str(month) + '_Climatology_Weekly.nc'
    s2s.writeInterim(output_file,int_filename,erai_clim,range(0,len(weeks)),range(start_year,end_year+1),lats,lons,'Climatology')