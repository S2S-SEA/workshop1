import netCDF4
import datetime

def save_netcdf(dest_dir,var_name,init_date,var_lat,var_lon,lead_times,var_hd,var_st,var_units,var_longname,arr_wkly,step_start,step_skip):
    # Define output file destination
    ds_out = netCDF4.Dataset(dest_dir + "ECMWF_" + var_name + "_2016-" + init_date + '_weekly.nc', 'w',format='NETCDF4_CLASSIC')

    # Create all the required dimensions of the variable 
    latitude = ds_out.createDimension('latitude', len(var_lat))
    longitude = ds_out.createDimension('longitude', len(var_lon))
    step = ds_out.createDimension('step', lead_times)
    time = ds_out.createDimension('time', len(var_hd))

    # Create the variables to store the data
    times = ds_out.createVariable('time', 'f8', ('time',))
    steps = ds_out.createVariable('step', 'f4', ('step',))
    latitudes = ds_out.createVariable('latitude', 'f4', ('latitude',))
    longitudes = ds_out.createVariable('longitude', 'f4', ('longitude',))
    # Create the 4-d variable
    nc_var = ds_out.createVariable(var_name, 'f4', ('time','step','latitude','longitude',),)

    # Define the properties of the variables
    times.units = 'hours since 2016-' + init_date + ' 00:00:00.0';

    times.calendar = 'standard';
    latitudes.units= 'degrees_north'
    longitudes.units= 'degrees_east'
    nc_var.units = var_units
    nc_var.missing_value= -32767
    nc_var.long_name = var_longname

    # Format the time variable
    var_time = [];
    for i in range(0,len(var_hd)):
        var_time.append(datetime.datetime(year=int(str(var_hd[i])[0:4]), month=int(str(var_hd[i])[4:6]), day=int(str(var_hd[i])[6:8])))

    # Populate the variables
    latitudes[:] = var_lat
    longitudes[:] = var_lon
    times[:] = netCDF4.date2num(var_time, units=times.units, calendar=times.calendar);
    steps[:] = var_st[step_start::step_skip]
    nc_var[:,:,:,:] = arr_wkly[:,:,:,:]

    # File is saved to .nc once closed
    ds_out.close()
