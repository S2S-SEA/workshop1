import os
import numpy
import netCDF4
import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def find_point(data_lat,data_lon,lat_down,lat_up,lon_left,lon_right):

    #Find the nearest points
    lat_index1 = numpy.where(data_lat == data_lat.flat[numpy.abs(data_lat - lat_down).argmin()])
    lat_index2 = numpy.where(data_lat == data_lat.flat[numpy.abs(data_lat - lat_up).argmin()])
    lon_index1 = numpy.where(data_lon == data_lon.flat[numpy.abs(data_lon - lon_left).argmin()])
    lon_index2 = numpy.where(data_lon == data_lon.flat[numpy.abs(data_lon - lon_right).argmin()])
    L1 = lat_index1[0][0]
    R1 = lat_index2[0][0]
    L2 = lon_index1[0][0]
    R2 = lon_index2[0][0]

    return L1,R1,L2,R2

def read_trmm(cur_trmm_path):

    #Open TRMM path to retreive data
    nc = netCDF4.Dataset(cur_trmm_path)
    prcpvar = nc.variables['precipitation']

    #Read TRMM time, latitude and longitude and data
    time_var = nc.variables['T']
    data_time = netCDF4.num2date(time_var[:],time_var.units)
    trmm_lat = nc.variables['Y'][:]
    trmm_lon = nc.variables['X'][:]
    trmm_data = prcpvar[:,:,:]    #time,lat,lon

    #Store TRMM time
    trmm_time = []
    for i in range(0,len(data_time)):
        trmm_time.append(data_time[i])

    return trmm_time,trmm_lat,trmm_lon,trmm_data
    nc.close()

def read_ec(cur_ec_path):

    #Open ECMWF path to retreive data
    nc = netCDF4.Dataset(cur_ec_path)
    prcpvar = nc.variables['prec']
    pdata = prcpvar[:,:,:,:]    #time,step,lat,lon

    #Read ECMWF time, step and data
    time_var = nc.variables['time']
    data_time = netCDF4.num2date(time_var[:],time_var.units)
    ec_time = data_time[::-1]    #reverse time
    ec_step = nc.variables['step'][:]
    ec_data = pdata[::-1,:,::-1,:]    #reserve time/lat

    return ec_time,ec_step,ec_data
    nc.close()

def read_anomaly(cur_data_path,index):

    #Open data path to retreive data
    nc = netCDF4.Dataset(cur_data_path)
    prcpvar = nc.variables['rainfall']

    #Read latitude and longitude and data
    data_lat = nc.variables['latitude'][:]
    data_lon = nc.variables['longitude'][:]
    if index == 'TRMM':
       pdata = prcpvar[:,:,:,:]    #week,year,lat,lon
    if index == 'ECMWF':
       pdata = prcpvar[:,:,:,:,:]    #step,week,year,lat,lon

    return data_lat,data_lon,pdata
    nc.close()

def write_trmm(trmm_output,trmm_filename,trmm_data,trmm_week,trmm_year,trmm_lat,trmm_lon,index):

    #Create output path
    if os.path.exists(trmm_output) == False:
       os.makedirs(trmm_output);
    nc = netCDF4.Dataset(trmm_output + '/' + trmm_filename,'w',format='NETCDF4_CLASSIC')

    #Create dimensions of variables
    week = nc.createDimension('week',len(trmm_week))
    latitude = nc.createDimension('latitude',len(trmm_lat))
    longitude = nc.createDimension('longitude',len(trmm_lon))
    if index == 'Average' or index == 'Anomaly':
       year = nc.createDimension('year',len(trmm_year))

    #Create variables
    weeks = nc.createVariable('week','f4',('week',))
    latitudes = nc.createVariable('latitude','f4',('latitude',))
    longitudes = nc.createVariable('longitude','f4',('longitude',))
    if index == 'Average' or index == 'Anomaly':
       years = nc.createVariable('year','f4',('year',)) 
       rainfall = nc.createVariable('rainfall','f4',('week','year','latitude','longitude',))
    if index == 'Climatology':
       rainfall = nc.createVariable('rainfall','f4',('week','latitude','longitude',))

    #Define properties of variables
    latitudes.units = 'degrees_north'  
    longitudes.units = 'degrees_east'  
    rainfall.units = 'mm/day'
    rainfall.long_name = 'Rainfall ' + index

    #Populate variables
    latitudes[:] = trmm_lat   
    longitudes[:] = trmm_lon
    weeks[:] = trmm_week
    if index == 'Average' or index == 'Anomaly':
       years[:] = trmm_year
       rainfall[:,:,:,:] = trmm_data
    if index == 'Climatology':
       rainfall[:,:,:] = trmm_data
    nc.close()

def write_ec(ec_output,ec_filename,ec_data,ec_step,ec_week,ec_year,ec_lat,ec_lon,index):

    #Create output path
    if os.path.exists(ec_output) == False:
       os.makedirs(ec_output);
    nc = netCDF4.Dataset(ec_output + '/' + ec_filename,'w',format='NETCDF4_CLASSIC')

    #Create dimensions of variables
    step = nc.createDimension('step',len(ec_step)) 
    week = nc.createDimension('week',len(ec_week))
    latitude = nc.createDimension('latitude',len(ec_lat))
    longitude = nc.createDimension('longitude',len(ec_lon))
    if index == 'Average' or index == 'Anomaly':
       year = nc.createDimension('year',len(ec_year))

    #Create variables
    steps = nc.createVariable('step','f4',('step',))
    weeks = nc.createVariable('week','f4',('week',))
    latitudes = nc.createVariable('latitude','f4',('latitude',))
    longitudes = nc.createVariable('longitude','f4',('longitude',))
    if index == 'Average' or index == 'Anomaly':
       years = nc.createVariable('year','f4',('year',)) 
       rainfall = nc.createVariable('rainfall','f4',('step','week','year','latitude','longitude',))
    if index == 'Climatology':
       rainfall = nc.createVariable('rainfall','f4',('step','week','latitude','longitude',))

    #Define properties of variables
    latitudes.units = 'degrees_north'  
    longitudes.units = 'degrees_east'  
    rainfall.units = 'mm/day'
    rainfall.long_name = 'Rainfall ' + index

    #Populate variables
    steps[:] = ec_step
    latitudes[:] = ec_lat   
    longitudes[:] = ec_lon
    weeks[:] = ec_week
    if index == 'Average' or index == 'Anomaly':
       years[:] = ec_year
       rainfall[:,:,:,:,:] = ec_data
    if index == 'Climatology':
       rainfall[:,:,:,:] = ec_data
    nc.close()

def plot_processing(data_0,lat_0,lon_0,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,data_range,title_str,name_str,index):

    #Find borders of the domain
    L1,R1,L2,R2 = find_point(lat_0,lon_0,lat_down,lat_up,lon_left,lon_right)
    lat_0 = lat_0 - 0.5*(lat_0[1]-lat_0[0])
    lon_0 = lon_0 - 0.5*(lon_0[1]-lon_0[0])
    lat = lat_0[L1:R1+1]
    lon = lon_0[L2:R2+1]
    latcorners = [lat.min(),lat.max()]
    loncorners = [lon.min(),lon.max()]

    #Add basemap
    #For map resolution, there are five options: c(crude),l(low),i(intermediate),h(high),f(full)
    #Higher resolution requires more time, defalut using low resolution
    m = Basemap(projection='merc',llcrnrlon=loncorners[0],llcrnrlat=latcorners[0],urcrnrlon=loncorners[1],urcrnrlat=latcorners[1],resolution='l')
    m.drawmapboundary()
    m.drawcoastlines()
    m.drawcountries()

    #Draw parallels and meridians
    parallels = numpy.arange(lat_down,lat_up,grid_lat)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=12)
    meridians = numpy.arange(lon_left,lon_right,grid_lon)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=12)

    #Compute map proj coordinates
    data = data_0[L1:R1+1,L2:R2+1]
    ny = data.shape[0]
    nx = data.shape[1]
    lons,lats = m.makegrid(nx,ny)
    x,y = m(lons,lats)

    #Specify colormaps
    if index == 'Climatology' or index == 'Average':
       cmap = plt.cm.gist_earth_r
    if index == 'Anomaly':
       cmap = plt.cm.BrBG

    #Plotting
    cs = m.pcolormesh(x,y,data,cmap=cmap)
    #Define data range
    cs.set_clim(data_range[0],data_range[1])
    #Add colorbar
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    cbar.set_label('mm/day',fontsize=13)

    #Add title and save figures
    plt.title(title_str,fontsize=13)
    plt.savefig(name_str,dpi=200,bbox_inches='tight')
    plt.close()

def plot_verification(data_0,lat_0,lon_0,lat_down,lat_up,lon_left,lon_right,grid_lat,grid_lon,title_str,name_str,index):

    #Find borders of the domain
    L1,R1,L2,R2 = find_point(lat_0,lon_0,lat_down,lat_up,lon_left,lon_right)
    lat_0 = lat_0 - 0.5*(lat_0[1]-lat_0[0])
    lon_0 = lon_0 - 0.5*(lon_0[1]-lon_0[0])
    lat = lat_0[L1:R1+1]
    lon = lon_0[L2:R2+1]
    latcorners = [lat.min(),lat.max()]
    loncorners = [lon.min(),lon.max()]

    #Add basemap
    #For map resolution, there are five options: c(crude),l(low),i(intermediate),h(high),f(full)
    #Higher resolution requires more time, defalut using low resolution
    m = Basemap(projection='merc',llcrnrlon=loncorners[0],llcrnrlat=latcorners[0],urcrnrlon=loncorners[1],urcrnrlat=latcorners[1],resolution='l')
    m.drawmapboundary()
    m.drawcoastlines()
    m.drawcountries()

    #Draw parallels and meridians
    parallels = numpy.arange(lat_down,lat_up,grid_lat)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=12)
    meridians = numpy.arange(lon_left,lon_right,grid_lon)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=12)

    #Compute map proj coordinates
    data = data_0[L1:R1+1,L2:R2+1]
    ny = data.shape[0]
    nx = data.shape[1]
    lons,lats = m.makegrid(nx,ny)
    x,y = m(lons,lats)

    #Create discrete colormap
    if index == 'CORA':
       cmap = mpl.colors.ListedColormap([(0.7451,0.8627,1),(0.9216,0.9216,0.9216),(1,0.9804,0.4902),(1,0.8235,0.8235),(1,0.6863,0.6863),(1,0.4902,0.4902),(1,0.1529,0.1529),(0.8235,0,0),(0.5961,0,0),(0.4510,0,0),(0.2941,0,0)])
       bounds = [-1,0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    if index == 'MSSS':
       cmap = mpl.colors.ListedColormap([(0.6863,0.6863,1),(0.7451,0.8627,1),(0.8235,0.8235,0.8235),(1,0.9294,0.9294),(1,0.8235,0.8235),(1,0.6863,0.6863),(1,0.4902,0.4902),(1,0.1569,0.1569),(0.8235,0,0),(0.5961,0,0)])
       bounds = [data.min(),-1,0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,1]
    norm = mpl.colors.BoundaryNorm(bounds,cmap.N)

    #Plotting
    cs = m.pcolormesh(x,y,data,cmap=cmap,norm=norm)
    #Add colorbar
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    if index == 'CORA':
       cbar.set_ticks([0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
       cbar.set_ticklabels(['0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1'])
    if index == 'MSSS':
       cbar.set_ticks([-1,0,0.05,0.1,0.2,0.3,0.4,0.5,0.6,1])
       cbar.set_ticklabels(['-1','0','0.05','0.1','0.2','0.3','0.4','0.5','0.6','1'])

    #Add title and save figures
    plt.title(title_str,fontsize=13)
    plt.savefig(name_str,dpi=200,bbox_inches='tight')
    plt.close()
