'''
This program processes the downloaded perturbed forecast (pf) and control
forecast dataset (cf). It combines the 10 ensembles members of ECMWF's pf 
with the 1 ECMWF's cf. The ensemble members are then averaged to provide
a single ensemble mean value. The temperature forecast for each week
(lead time) is calculated by averaging all the time steps in that week. The files are then saved to an output netCDF file for the next stage of processing. 
'''
import netCDF4
import numpy as np
import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/' + '../../../utils/')
import s2s_utils_comm as ucomm

vtype = 0 # 0: tmin, 1: tmax
vsuffx = ['tmin','tmax']
vname = ['mn2t6','mx2t6']

# Define data folder
dest_dir = '../../../../data/model/ecmwf/tminmax/'
no_of_wks = 4

# All the initial dates with complete 7-day week in Nov for the 2016 runs
init_date = ['10-13','10-17','10-20','10-24','10-27','10-31','11-03','11-07','11-10','11-14','11-17','11-21','11-24']

# For each initial date file
for i_date in range(0,len(init_date)):
    print("Processing initial date:",init_date[i_date])
    ds_pf = netCDF4.Dataset(dest_dir + "ECMWF_" + vsuffx[vtype] + "_2016-" + init_date[i_date] + '_pf.nc') # Load the pf file
    ds_cf = netCDF4.Dataset(dest_dir + "ECMWF_" + vsuffx[vtype] + "_2016-" + init_date[i_date] + '_cf.nc') # Load the cf file

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
  
    # Read in the array from pf's sfctemp min or max ('mn2t6' or 'mx2t6') variable
    arr_pf = ds_pf.variables[vname[vtype]][:]
    # Read in the cf's total sfctemp ('t2m') variable
    arr_cf = ds_cf.variables[vname[vtype]][:]

    arr_shp = arr_pf.shape
    # Create a new array to accommodate the 10 pf and 1 cf members
    arr_comb = np.empty([arr_shp[0], arr_shp[1], arr_shp[2]+1, arr_shp[3], arr_shp[4]])
    # Populate arr_comb with pf and cf data
    arr_comb[:,:,0:10,:,:] = arr_pf
    arr_comb[:,:,10,:,:] = arr_cf

    # Average over the ensemble axis/dimension
    arr_ens_avg = np.mean(arr_comb, axis=2)

    # Calculate daily max/min first, then calculate weekly average of max/min
    arr_daily = np.empty([arr_shp[0], no_of_wks*7, arr_shp[3], arr_shp[4]])
    arr_wkly = np.empty([arr_shp[0], no_of_wks, arr_shp[3], arr_shp[4]])
    for day in range(no_of_wks*7):
        #print("Calculating for day: ", day)
        if vtype == 0:
            # Calculate for each day the min
            arr_daily[:,day,:,:] = np.amin(arr_ens_avg[:,(day*4):((day+1)*4),:,:], axis=1)
        else:
            # Calculate for each day the max
            arr_daily[:,day,:,:] = np.amax(arr_ens_avg[:,(day*4):((day+1)*4),:,:], axis=1)
            
    for week in range(no_of_wks):
        #print("Calculating average for week: ", week)
        arr_wkly[:,week,:,:] = np.mean(arr_daily[:,(week*7):(week*7+7),:,:], axis=1) # Average over the week


    #-------------------------------------
    # Output variable to netCDF
    #-------------------------------------
    # Define output file destination
    ucomm.save_netcdf(dest_dir,vsuffx[vtype],init_date[i_date],temp_lat,temp_lon,no_of_wks,temp_hd,temp_st,'K','2 m ' + vsuffx[vtype] + ' daily temperature',arr_wkly,step_start=27,step_skip=28)  
  
    '''
    ds_out = netCDF4.Dataset(dest_dir + "ECMWF_" + vsuffx[vtype] + "_2016-" + init_date[i_date] + '_weekly.nc', 'w',format='NETCDF4_CLASSIC')

    # Create all the required dimensions of the variable 
    latitude = ds_out.createDimension('latitude', len(temp_lat))
    longitude = ds_out.createDimension('longitude', len(temp_lon))
    step = ds_out.createDimension('step', no_of_wks) 
    time = ds_out.createDimension('time', len(temp_hd))    

    # Create the variables to store the data
    times = ds_out.createVariable('time', 'f8', ('time',)) 
    steps = ds_out.createVariable('step', 'f4', ('step',)) 
    latitudes = ds_out.createVariable('latitude', 'f4', ('latitude',))
    longitudes = ds_out.createVariable('longitude', 'f4', ('longitude',)) 
    # Create the 4-d temperature variable
    sfctemp = ds_out.createVariable(vsuffx[vtype], 'f4', ('time','step','latitude','longitude',),) 

    # Define the properties of the variables
    times.units = 'hours since 2016-' + init_date[i_date] + ' 00:00:00.0';
    times.calendar = 'standard';
    latitudes.units= 'degrees_north'  
    longitudes.units= 'degrees_east'  
    sfctemp.units = 'K'
    sfctemp.missing_value= -32767
    if vtype == 0:
        sfctemp.long_name = '2 m min temperature'
    else:
        sfctemp.long_name = '2 m max temperature'

    # Format the time variable
    temp_time = [];
    for i in range(0,len(temp_hd)):
        temp_time.append(datetime.datetime(year=int(str(temp_hd[i])[0:4]), month=int(str(temp_hd[i])[4:6]), day=int(str(temp_hd[i])[6:8])))
    
    # Populate the variables
    latitudes[:] = temp_lat   
    longitudes[:] = temp_lon
    times[:] = netCDF4.date2num(temp_time, units=times.units, calendar=times.calendar);
    steps[:] = temp_st[27::28]  
    sfctemp[:,:,:,:] = arr_wkly[:,:,:,:]

    # File is saved to .nc once closed
    ds_out.close()  

    '''
    ds_pf.close()
    ds_cf.close()
