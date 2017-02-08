'''
#DRAFT VERSION
Need to add comments
Need to check that the date lists match the dates from the interim and ecmwf files (right now will probably crash if they don't)
Need to un-hard code the starting point in the list
Need to change the cora file to store all weeks 

'''
#this is calculating CORA 
import datetime
import numpy as np
from scipy import interpolate
import processInterimFun as pf
import s2sUtilitiesThea as s2s
#import read_ecmwf
#import plot_figure_cora

##--------------------------------------------SPECIFY--------------------------------------------------------------
model_initial_date = ['1013','1017','1020','1024','1027','1031','1103','1107','1110','1114','1117','1121','1124']
initDate = [3,7,10,14,17,21,24] 
startYear = 1998
endYear = 2014
model_step = 4
ec_input = '../../workshop1/data/model/ecmwf/temp' # will need to change this path 

#the domain
lat_up = 30
lat_down = -20
lon_left = 85.5
lon_right = 150
##--------------------------------------------PROCESSING---------------------------------------------------------

intLon, intLat, intDateList, intAnom= pf.processInterim(11, initDate, startYear, endYear, 3)
lat_index2 = np.where(intLat == intLat.flat[np.abs(intLat - lat_up).argmin()])[0] # need to make this into a function
lat_index1 = np.where(intLat == intLat.flat[np.abs(intLat - lat_down).argmin()])[0]
lon_index1 = np.where(intLon == intLon .flat[np.abs(intLon  - lon_left).argmin()])[0]
lon_index2 = np.where(intLon  == intLon .flat[np.abs(intLon  - lon_right).argmin()]) [0]
print(lat_index1)
intLat = intLat[lat_index1[0]:lat_index2[0]]
intLon = intLon[lon_index1[0]:lon_index2[0]]
intAnom = intAnom[:,:, lat_index1[0]:lat_index2[0],lon_index1[0]:lon_index2[0]]


print(intLat[0], intLat[1], intLat[-1]) #84, 85.5, 156
print(intLon[0], intLon[1], intLon[-1])#-25, -24, 36
print(intDateList[0], intDateList[1], intDateList[-1]) #1998-11-03, 11-07, 11-24
ecWeekly = np.empty([model_step, endYear+1-startYear, len(model_initial_date),len(intLat), len(intLon)])
ecAnom = np.empty([model_step, endYear+1-startYear, len(model_initial_date),len(intLat), len(intLon)])
ecClimo = np.empty([model_step, len(model_initial_date),len(intLat), len(intLon)])
print( ecAnom.shape, ecWeekly.shape, ecClimo.shape)

for i_step in range(0,model_step):
    sum_ec_trmm = np.zeros([len(intLat),len(intLon)]);
    sum_ec = np.zeros([len(intLat),len(intLon)]);
    sum_trmm = np.zeros([len(intLat),len(intLon)]);
    
    for i_date in range(0,len(model_initial_date)):
        model_date = model_initial_date[i_date]
        cur_ec_filename = 'ECMWF_temp_2016-' + model_date[:2] + '-' + model_date[-2:] + '_weekly.nc'
    #no interpolation needed, just need to make sure they are the right way around (which they are not)
        dataLat, dataLon, dataTime, dataStep, ectemp= s2s.getECMWFweeklly(ec_input + '/' + cur_ec_filename)

        ## NEED TO ADD A CHECK THAT THE DATES FROM THE MODEL ARE THE SAME AS THE ONES WRITTEN ABOVE...ALSO FOR INTERIM
        lat_index2 = np.where(dataLat == dataLat.flat[np.abs(dataLat - lat_up).argmin()])[0]
        lat_index1 = np.where(dataLat == dataLat.flat[np.abs(dataLat - lat_down).argmin()])[0]
        lon_index1 = np.where(dataLon == dataLon.flat[np.abs(dataLon - lon_left).argmin()])[0]
        lon_index2 = np.where(dataLon == dataLon.flat[np.abs(dataLon - lon_right).argmin()]) [0]

        ectemp = ectemp[:-1,:, lat_index1[0]:lat_index2[0],lon_index1[0]:lon_index2[0]]

        ecWeekly[i_step, :, i_date, :, :] = ectemp[:, i_step, :, :]
        #getting the climatology for a particular week and timestep.
        ecClimo[i_step,  i_date, :, :] = np.mean(ectemp[:, i_step, :, :], axis = 0)
        #getting the anomaly values
        print( ecAnom[i_step, :, i_date, :, :].shape, ecWeekly[i_step, :, i_date, :, :].shape, ecClimo[i_step, i_date, :, :].shape)
        ecAnom[i_step, :, i_date, :, :] = ecWeekly[i_step, :, i_date, :, :] - ecClimo[i_step, i_date, :, :]

        # now need to caluclate CORA & MSS. 

        ##need to find the startLocation and endLocation for the week files
        startLoc = 7-i_step # needs to be changed from hard code
        endLoc = 14-i_step

        count = 0
        if i_date >= startLoc and i_date < endLoc :
           sum_ec_trmm = sum_ec_trmm + np.sum(ecAnom[i_step, :, i_date, :, :]*intAnom[:, count, :, :], axis = 0)
           sum_ec = sum_ec + np.sum(ecAnom[i_step, :, i_date, :, :]**2, axis =0)
           sum_trmm = sum_trmm + np.sum(intAnom[:, count, :, :]**2, axis = 0)
           count +=1 


    #Calculate CORA
    cora = sum_ec_trmm/(sum_ec**(1.0/2)*sum_trmm**(1.0/2))
    print(cora[10, 20], np.max(cora))

      
       