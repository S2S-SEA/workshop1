#these are the basic functions for my scripts!
#those for the plots
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset

#those for loading data
from netCDF4 import Dataset, num2date

def getInterim(filename) :
##Input data information:
    #just the file name where the netCDF file is stored
##Return data information:
    #the longitude and latidute of the dataset
    #the time as a numpy array (times) in datetime format
    # the data itself
    nc = Dataset(filename, mode ='r')
    lons = nc.variables['longitude'][:] # 49, degrees east
    lat =  nc.variables['latitude'][:] # 42, degrees_north
    lats = np.flipud(lat)# have to flip, lats go the other way!
    timeRaw =  nc.variables['time'] #128, hours since 1900-01-01, 00:00:00
    times  = num2date(timeRaw[:],timeRaw.units)
    dataTemp =  nc.variables['t2m'][:]# time, latitude, longitude, K
    data = dataTemp[:,::-1, :] # have to flip, lats go the other way!
    nc.close ()
    return lons, lats, times, data

def getECMWFweekly(filename): 
    ##Input data information:
    #just the file name where the netCDF file is stored
##Return data information:
    #the longitude and latidute of the dataset
    #the time as a numpy array (times) in datetime format
    # the data itself
    nc = Dataset(filename)
    dataLat = nc.variables['latitude'][:] 
    dataLat = dataLat[::-1]
    dataLon = nc.variables['longitude'][:]
    timeRaw = nc.variables['time']
    dataTime  = num2date(timeRaw[:],timeRaw.units)
    dataTime = dataTime[::-1]
    dataStep = nc.variables['step'][:]
    dataTemp= nc.variables['sfctemp'][:]
#    data = dataTemp[:,:,::-1, :] # have to flip, lats go the other way!
    ecTemp = dataTemp[::-1,:, ::-1, :]
    nc.close()

    # now getting it in the correct format, so that only the weeks in the period are included

    return dataLat, dataLon, dataTime, dataStep, ecTemp


def makeSmaller(lats, lons, lat_up, lat_down, lon_left, lon_right):
    #Finds the closest point for latitude and longitude values. 
   
    lat_index2 = np.where(lats == lats.flat[np.abs(lats - lat_up).argmin()])[0] # need to make this into a function
    lat_index1 = np.where(lats == lats.flat[np.abs(lats - lat_down).argmin()])[0]
    lon_index1 = np.where(lons == lons .flat[np.abs(lons  - lon_left).argmin()])[0]
    lon_index2 = np.where(lons  == lons .flat[np.abs(lons  - lon_right).argmin()]) [0]
    lats = lats[lat_index1[0]:lat_index2[0]+1]
    lons = lons[lon_index1[0]:lon_index2[0]+1]
  
    return lat_index1[0], lat_index2[0], lon_index1[0], lon_index2[0], lats, lons

def plot_figure(data_0,lat_0,lon_0,dataLimit, title_str, name_str, index):
##Input data information:
    #data_0 = the temperature file that want to plot. Should be in format data[len(lat_0), len(lon_0)]
    #lat_0 = latitude 
    #lon_0 = longitude
    #title_str & name_str = the title refers to the plot, '' will have no title, and name_str is how it will be saved. 
    #dataLimit = the maximum and minimum values for the colorbar in format [min, max]
    #index = Climatology, Anomaly, Average - one of these three (will alter the title)
## Return data information:
    # No data is return. Only one file is saved

    #Caculate borders for the domain
    latcorners = [lat_0.min(),lat_0.max()]
    loncorners = [lon_0.min(),lon_0.max()]

    #Add basemap
    m = Basemap(projection='merc',llcrnrlon=loncorners[0],llcrnrlat=latcorners[0],urcrnrlon=loncorners[1],urcrnrlat=latcorners[1],resolution='l',area_thresh=10)
    m.drawmapboundary()
    m.drawcoastlines()
    m.drawcountries()

    #Draw parallels and meridians
    parallels = np.arange(lat_0.min(),lat_0.max(),10)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=12)
    meridians = np.arange(lon_0.min(),lon_0.max(),10)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=12)

    #Compute map proj coordinates
    data = data_0
    ny = data.shape[0]
    nx = data.shape[1]
    lons,lats = m.makegrid(nx,ny)
    x,y = m(lons,lats)

    #Specify colormaps
    if index == 'Climatology' or index == 'Average':
       cmap = plt.cm.coolwarm
    elif index == 'Anomaly':
       cmap = plt.cm.bwr
    else:
       cmap = plt.cm.coolwarm
   
       #Plotting
    cs = m.pcolormesh(x,y,data,cmap=cmap)

    #Define data range
    cs.set_clim(dataLimit[0],dataLimit[1])

    #Add colorbar
    cbar = m.colorbar(cs,location='bottom',pad="5%")
    cbar.set_label('K',fontsize=13)



    #Add title and save figures
    plt.title(title_str,fontsize=13)
    plt.savefig(name_str,dpi=200,bbox_inches='tight')
    plt.close()

def writeInterim(ec_output,ec_filename,ec_data,ec_week,ec_year,ec_lat,ec_lon,index):
    #INPUT:
# ec_output= the file path to where you want to save the data
#ec_filename = the file name to save to
#ec_data = the temperature data (e.g. interimAnom)
#ec_week =  a list of the weeks
#ec_year = a list of the years
#ec_lat = the latitude values
#ec_lon = the longitude values
#index = either Average, Anomaly, or Climatology. Make sure it matches the data!
    #Create output path
    if os.path.exists(ec_output) == False:
       os.makedirs(ec_output);
    nc = Dataset(ec_output + '/' + ec_filename,'w',format='NETCDF4_CLASSIC')

    #Create dimensions of variables
    week = nc.createDimension('week',len(ec_week))
    latitude = nc.createDimension('latitude',len(ec_lat))
    longitude = nc.createDimension('longitude',len(ec_lon))
    if index == 'Average' or index == 'Anomaly':
       year = nc.createDimension('year',len(ec_year))

    #Create variables
    weeks = nc.createVariable('week','f4',('week',))
    latitudes = nc.createVariable('latitude','f4',('latitude',))
    longitudes = nc.createVariable('longitude','f4',('longitude',))
    if index == 'Average' or index == 'Anomaly':
       years = nc.createVariable('year','f4',('year',)) 
       sfctemp = nc.createVariable('sfctemp','f4',('week','year','latitude','longitude',))
    if index == 'Climatology':
       sfctemp = nc.createVariable('sfctemp','f4',('week','latitude','longitude',))

    #Define properties of variables
    latitudes.units = 'degrees_north'  
    longitudes.units = 'degrees_east'  
    sfctemp.units = 'K'
    sfctemp.long_name = 'SfcTemp ' + index

    #Populate variables
    latitudes[:] = ec_lat   
    longitudes[:] = ec_lon
    weeks[:] = ec_week
    if index == 'Average' or index == 'Anomaly':
       years[:] = ec_year
       sfctemp[:,:,:,:] = ec_data
    if index == 'Climatology':
       sfctemp[:,:,:] = ec_data
    nc.close()


def write_ec(ec_output,ec_filename,ec_data,ec_step,ec_week,ec_year,ec_lat,ec_lon,index):
    '''
    Write the ECMWF data to a specfic file
    ec_output: where to save to
    ec_filename: the name of the file
    ec_data = the temperature data
    ec_step = the lead times
    ec_year = the years
    ec_week = the start days for the weeks
    ec_lat/lon = latitude and longitude files
    index ='Average', 'Anomaly' or 'Climatology'
    '''
    #Create output path
    if os.path.exists(ec_output) == False:
       os.makedirs(ec_output);
    nc = Dataset(ec_output + '/' + ec_filename,'w',format='NETCDF4_CLASSIC')

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
       sfctemp = nc.createVariable('sfctemp','f4',('step','week','year','latitude','longitude',))
    if index == 'Climatology':
       sfctemp = nc.createVariable('sfctemp','f4',('step','week','latitude','longitude',))

    #Define properties of variables
    latitudes.units = 'degrees_north'  
    longitudes.units = 'degrees_east'  
    sfctemp.units = 'K'
    sfctemp.long_name = 'SfcTemp ' + index

    #Populate variables
    steps[:] = ec_step
    latitudes[:] = ec_lat   
    longitudes[:] = ec_lon
    weeks[:] = ec_week
    if index == 'Average' or index == 'Anomaly':
       years[:] = ec_year
       sfctemp[:,:,:,:,:] = ec_data
    if index == 'Climatology':
       sfctemp[:,:,:,:] = ec_data
    nc.close()




def plot_verification(data,lat,lon,grid_lat,grid_lon,title_str,name_str,index):
    '''
    Input:
    data_0 0 the data that you want to plot
    lat_0/lon_0 - the latitude/longitude  values
    grid_lat/lon: the number of gride lines you want
    title_str : the title for the plot
    name_str: the name of the file to save to
    index: either 'MSSS'or 'CORA'
    Return
    No data is returned. Only 1 file saved. 
    '''
    #Find borders of the domain
    lat_down = lat.min()
    lat_up = lat.max()
    lon_left = lon.min()
    lon_right = lon.max()
    latcorners = [lat_down,lat_up]
    loncorners = [lon_left,lon_right]

    #Add basemap
    #For map resolution, there are five options: c(crude),l(low),i(intermediate),h(high),f(full)
    #Higher resolution requires more time, defalut using low resolution
    m = Basemap(projection='merc',llcrnrlon=loncorners[0],llcrnrlat=latcorners[0],urcrnrlon=loncorners[1],urcrnrlat=latcorners[1],resolution='l')
    m.drawmapboundary()
    m.drawcoastlines()
    m.drawcountries()

    #Draw parallels and meridians
    parallels = np.arange(lat_down,lat_up,grid_lat)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=12)
    meridians = np.arange(lon_left,lon_right,grid_lon)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=12)

    #Compute map proj coordinates
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

