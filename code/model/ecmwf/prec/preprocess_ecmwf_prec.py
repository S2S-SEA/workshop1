'''
This program processes the downloaded perturbed forecast (pf) and control
forecast dataset (cf). It combines the 10 ensembles members of ECMWF's pf 
with the 1 ECMWF's cf. The ensemble members are then averaged to provide
a single ensemble mean value. The precipitation forecast for each week
(lead time) is calculated by substracting the end points of each time step
for the weekly total and then dividing by seven to get the daily average
for each week. The files are then saved to an output netCDF file for the
next stage of processing. 
'''
import netCDF4
import numpy as np
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/' + '../../../utils/')
import s2s_utils_comm as ucomm
#print("path: ",os.path.abspath(os.path.dirname(__file__)) + '/' + '../../../utils/')

# Define data folder
dest_dir = '../../../../data/model/ecmwf/prec/'
no_of_weeks = 4

# All the initial dates with complete 7-day week in Nov for the 2016 runs
init_date = ['10-13','10-17','10-20','10-24','10-27','10-31','11-03','11-07','11-10','11-14','11-17','11-21','11-24']

# For each initial date file
for i_date in range(0,len(init_date)):
    print("Processing initial date:",init_date[i_date])
    ds_pf = netCDF4.Dataset(dest_dir + "ECMWF_prec_2016-" + init_date[i_date] + '_pf.nc') # Load the pf file
    ds_cf = netCDF4.Dataset(dest_dir + "ECMWF_prec_2016-" + init_date[i_date] + '_cf.nc') # Load the cf file

    # You may want to uncomment the following lines
    # to print out the file and variable information
    #print(ds_pf.file_format)
    #print(ds_pf.dimensions.keys())
    #print(ds_pf.variables)

    # Read in the variables from cf
    prec_hd = ds_cf.variables['hdate'][:]
    prec_st = ds_cf.variables['step'][:]
    prec_lat = ds_cf.variables['latitude'][:]
    prec_lon = ds_cf.variables['longitude'][:]
  
    # Read in the array from pf's total precip ('tp') variable
    arr_pf = ds_pf.variables['tp'][:]
    # Read in the cf's total precip ('tp') variable
    arr_cf = ds_cf.variables['tp'][:]

    arr_shp = arr_pf.shape
    # Create a new array to accommodate the 10 pf and 1 cf members
    arr_comb = np.empty([arr_shp[0], arr_shp[1], arr_shp[2]+1, arr_shp[3], arr_shp[4]])
    # Populate arr_comb with pf and cf data
    arr_comb[:,:,0:10,:,:] = arr_pf
    arr_comb[:,:,10,:,:] = arr_cf

    # Average over the ensemble axis/dimension
    arr_ens_avg = np.mean(arr_comb, axis=2)

    # Calculate weekly totals
    arr_wkly = np.empty([arr_shp[0], arr_shp[1]-1, arr_shp[3], arr_shp[4]])
    for i in range(arr_ens_avg.shape[1]-1):
        arr_wkly[:,i,:,:] = np.subtract(arr_ens_avg[:,i+1,:,:], arr_ens_avg[:,i,:,:]) # Substract to get weekly totals
        arr_wkly[:,i,:,:] = arr_wkly[:,i,:,:]/7.0 # Divide by 7 for daily average
    #-------------------------------------
    # Output variable to netCDF
    #-------------------------------------
    # Define output file destination
    ucomm.save_netcdf(dest_dir,'prec',init_date[i_date],prec_lat,prec_lon,no_of_weeks,prec_hd,prec_st,'kg m**-2','Total Precipitation',arr_wkly,1,1)
    '''
    ds_out = netCDF4.Dataset(dest_dir + "ECMWF_prec_2016-" + init_date[i_date] + '_weekly.nc', 'w',format='NETCDF4_CLASSIC')

    # Create all the required dimensions of the variable 
    latitude = ds_out.createDimension('latitude', len(prec_lat))
    longitude = ds_out.createDimension('longitude', len(prec_lon))
    step = ds_out.createDimension('step', no_of_weeks) 
    time = ds_out.createDimension('time', len(prec_hd))    

    # Create the variables to store the data
    times = ds_out.createVariable('time', 'f8', ('time',)) 
    steps = ds_out.createVariable('step', 'f4', ('step',)) 
    latitudes = ds_out.createVariable('latitude', 'f4', ('latitude',))
    longitudes = ds_out.createVariable('longitude', 'f4', ('longitude',)) 
    # Create the 4-d precipitation variable
    precip = ds_out.createVariable('prec', 'f4', ('time','step','latitude','longitude',),) 

    # Define the properties of the variables
    times.units = 'hours since 2016-' + init_date[i_date] + ' 00:00:00.0';
    times.calendar = 'standard';
    latitudes.units= 'degrees_north'  
    longitudes.units= 'degrees_east'  
    precip.units = 'kg m**-2'
    precip.missing_value= -32767
    precip.long_name = 'Total Precipitation'

    # Format the time variable
    prec_time = [];
    for i in range(0,len(prec_hd)):
        prec_time.append(datetime.datetime(year=int(str(prec_hd[i])[0:4]), month=int(str(prec_hd[i])[4:6]), day=int(str(prec_hd[i])[6:8])))
    
    # Populate the variables
    latitudes[:] = prec_lat   
    longitudes[:] = prec_lon
    times[:] = netCDF4.date2num(prec_time, units=times.units, calendar=times.calendar);
    steps[:] = prec_st[1::1]  
    precip[:,:,:,:] = arr_wkly[:,:,:,:]

    # File is saved to .nc once closed
    ds_out.close()  
    '''
    ds_pf.close()
    ds_cf.close()
