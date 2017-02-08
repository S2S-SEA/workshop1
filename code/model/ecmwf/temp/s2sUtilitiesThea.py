#these are the basic functions for my scripts!
#those for the plots
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

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

def getECMWFweeklly(filename): 
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
    data = dataTemp[:,:,::-1, :] # have to flip, lats go the other way!
    ecTemp = dataTemp[::-1,:, :, :]
    nc.close()
    return dataLat, dataLon, dataTime, dataStep, ecTemp
def plot_figure(data_0,lat_0,lon_0,time_period,dataLimit,index):
##Input data information:
    #data_0 = the temperature file that want to plot. Should be in format data[len(lat_0), len(lon_0)]
    #lat_0 = latitude 
    #lon_0 = longitude
    #time_period = this is just for the name of the file where it is saved
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

    #Define title and name convention
    title_str = 'Temperature '+ index
    name_str = 'interim_' +time_period +'_' + index+'.png'

    #Add title and save figures
    plt.title(title_str,fontsize=13)
    plt.savefig(name_str,dpi=200,bbox_inches='tight')
    plt.close()
