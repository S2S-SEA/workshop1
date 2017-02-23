'''
This program processes the downloaded perturbed forecast (pf) and control
forecast dataset (cf). It combines the 10 ensembles members of ECMWF's pf 
with the 1 ECMWF's cf. The ensemble members are then averaged to provide
a single ensemble mean value. The temperature forecast for each week
(lead time) is calculated by averaging all the time steps in that week. The files are then saved to an output netCDF file for the
next stage of processing. 
'''
import netCDF4
import numpy as np
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/' + '../../../utils/')
import s2s_utils_comm as ucomm

# Define data folder
dest_dir = '../../../../data/model/ecmwf/temp/'
no_of_wks = 4

# All the initial dates with complete 7-day week in Nov for the 2016 runs
init_date = ['10-13','10-17','10-20','10-24','10-27','10-31','11-03','11-07','11-10','11-14','11-17','11-21','11-24']

# For each initial date file
for i_date in range(0,len(init_date)):
    print("Processing initial date:",init_date[i_date])
    ds_pf = netCDF4.Dataset(dest_dir + "ECMWF_temp_2016-" + init_date[i_date] + '_pf.nc') # Load the pf file
    ds_cf = netCDF4.Dataset(dest_dir + "ECMWF_temp_2016-" + init_date[i_date] + '_cf.nc') # Load the cf file

    # You may want to uncomment the following lines
    # to print out the file and variable information
    #print(ds_pf.file_format)
    #print(ds_pf.dimensions.keys())
    #print(ds_pf.variables)

    # Read in the variables from cf
    temp_hd = ds_cf.variables['hdate'][:]
    temp_st = ds_cf.variables['step'][:]
    temp_lat = ds_cf.variables['latitude'][:]
    temp_lon = ds_cf.variables['longitude'][:]

    # Read in the array from pf's sfctemp ('t2m') variable
    arr_pf = ds_pf.variables['t2m'][:]
    # Read in the cf's total sfctemp ('t2m') variable
    arr_cf = ds_cf.variables['t2m'][:]

    arr_shp = arr_pf.shape
    # Create a new array to accommodate the 10 pf and 1 cf members
    arr_comb = np.empty([arr_shp[0], arr_shp[1], arr_shp[2]+1, arr_shp[3], arr_shp[4]])
    # Populate arr_comb with pf and cf data
    arr_comb[:,:,0:10,:,:] = arr_pf
    arr_comb[:,:,10,:,:] = arr_cf

    # Average over the ensemble axis/dimension
    arr_ens_avg = np.mean(arr_comb, axis=2)

    # Calculate daily average for each week
    arr_wkly = np.empty([arr_shp[0], no_of_wks, arr_shp[3], arr_shp[4]])
    for i in range(no_of_wks):
        #print("Calculating for week: ", i)
        arr_wkly[:,i,:,:] = np.mean(arr_ens_avg[:,(i*7):(i*7+7),:,:], axis=1) # Average over the week
    
    #-------------------------------------
    # Output variable to netCDF
    #-------------------------------------
    # Define output file destination
    ucomm.save_netcdf(dest_dir,'temp',init_date[i_date],temp_lat,temp_lon,no_of_wks,temp_hd,temp_st,'K','2 m average daily temperature',arr_wkly,step_start=6,step_skip=7)
    ds_pf.close()
    ds_cf.close()
