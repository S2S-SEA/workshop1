'''
This script calculates CORA for temperature using ERA interim and model data. 
It calls the processInterim and processECMWF files to calculate the weekly anomalies. 
Make sure you check all the conditions und
'''
#this is calculating CORA 
import datetime
import numpy as np
from scipy import interpolate
import processFunctions as pf
import s2sUtilitiesThea as s2s

##--------------------------------------------SPECIFY--------------------------------------------------------------
model_initial_date = ['1013','1017','1020','1024','1027','1031','1103','1107','1110','1114','1117','1121','1124'] # this is the name of all the ECMWF files for the start dates
# make sure this list matches with the files you downloaded
initDate = [3,7,10,14,17,21,24] # these are the start dates for the weeks you are looking for. Make sure they match with the model data!
initMonth = 11 # this is the month you want to be looking at 
startYear = 1998 # start year
endYear = 2014 # end year
model_step = 4 # this is the number of lead time weeks 
ec_input = '../../workshop1/data/model/ecmwf/temp' # will need to change this path 

#the domain
lat_up = 30
lat_down = -20
lon_left = 85.5
lon_right = 150

#options
printData=[0,18,13] # set printData = 0 if nothing to print out, otherwise specify [model_step, latitude location, longitude location]
plotting = False# if true, the plots will be done and saved, no plots if false
##--------------------------------------------PROCESSING---------------------------------------------------------
#check print option
if printData != 0:
    if printData[0]>= model_step:
        printData[0] = input('Your model step is out of bounds. Please enter a number between 0 and '+ str(model_step-1))

#get the Interim data (similar to process script)
intLon, intLat, intDateList, intAnom= pf.processInterim(initMonth, initDate, startYear, endYear, 3)

intAnom, intLat, intLon = s2s.makeSmaller(intLat, intLon, lat_up, lat_down, lon_left, lon_right, intAnom, 4)

print("Interim data starting from " + str(intDateList[0]) + " to " + str(intDateList[-1])) #1998-11-03, 11-07, 11-24

if printData !=0:
    print('ERAIn Anomaly values')
    print(intAnom[ :, :, printData[1],printData[-1]])
# format is model step/forecast week,  latitude, longitude
cora = np.empty([model_step,len(intLat), len(intLon)])

dataLon, dataLat, ecAnom = pf.processEcmwfTemp(ec_input, model_initial_date, model_step, initMonth, initDate, startYear, endYear, 3)
ecAnom, dataLat, dataLon = s2s.makeSmaller(dataLat, dataLon, lat_up, lat_down, lon_left, lon_right, ecAnom, 5)

if printData !=0:
    print('ECMWF Anomaly values')
    print(ecAnom[printData[0], :, :, printData[1],printData[-1]])
for i_step in range(model_step):
   
        #CORA
        #this is working out the formula = sum(interimAnomaly*ecmwfAnomlay)/(sqrt(sum(interimAnomaly^2))*sqrt(sum(ecmwfAnomaly^2))
        sum_ec_trmm =np.sum(np.sum(ecAnom[i_step, :, :, :, :]*intAnom[:, :, :, :], axis = 0), axis = 0)
        sum_ec =  np.sum(np.sum(ecAnom[i_step, :, :, :, :]**2, axis =0), axis = 0)
        sum_trmm =  np.sum(np.sum(intAnom[:, :, :, :]**2, axis = 0), axis =0)

        #Calculate CORA
        cora[i_step, :, :] = sum_ec_trmm/(sum_ec**(1.0/2)*sum_trmm**(1.0/2))

if printData !=0:
    print('cora')
    print(cora[printData[0], printData[1],printData[-1]], np.max(cora[printData[0], printData[1],printData[-1]]))

      
       