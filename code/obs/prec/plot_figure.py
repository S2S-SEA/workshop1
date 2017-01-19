#This self-defined function is used for visualization.

import matplotlib as mpl
mpl.use('Agg')
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def plot_figure(data_0,lat_0,lon_0,start_date,end_date,month,year,index):

    #Caculate borders for the domain
    latcorners = [lat_0.min(),lat_0.max()];
    loncorners = [lon_0.min(),lon_0.max()];

    #Add basemap
    m = Basemap(projection='merc',llcrnrlon=loncorners[0],llcrnrlat=latcorners[0],urcrnrlon=loncorners[1],urcrnrlat=latcorners[1],resolution='h',area_thresh=10);
    m.drawmapboundary();
    m.drawcoastlines();
    m.drawcountries();

    #Draw parallels and meridians
    parallels = np.arange(-20.,30.,10);
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=12);
    meridians = np.arange(80.,150.,10);
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=12);

    #Compute map proj coordinates
    data = data_0;
    ny = data.shape[0]; 
    nx = data.shape[1];
    lons,lats = m.makegrid(nx,ny);
    x,y = m(lons,lats);

    #Specify colormaps
    if index == 'climatology' or index == 'average':
       cmap = plt.cm.gist_earth_r;
    if index == 'anomaly':
       cmap = plt.cm.BrBG;

    #Plotting
    cs = m.pcolormesh(x,y,data,cmap=cmap);

    #Define data range
    if index == 'climatology' or index == 'average':
       cs.set_clim(data.min(),data.max());
    if index == 'anomaly':
       data_range = min(abs(data.min()),data.max());
       cs.set_clim(-data_range,data_range);

    #Add colorbar
    cbar = m.colorbar(cs,location='bottom',pad="5%");
    cbar.set_label('mm/day',fontsize=13);

    #Define title and name convention
    if index == 'climatology':
       title_str = 'Rainfall Climatology';
       name_str = 'TRMM_' + month + '_' + start_date + '-' + end_date + '_' + 'Climatology.png';
    if index == 'average':
       title_str = 'Average Rainfall';
       name_str = 'TRMM_' + year + month + '_' + start_date + '-' + end_date + '_' + 'Average.png';
    if index == 'anomaly':
       title_str = 'Rainfall Anomaly';
       name_str = 'TRMM_' + year + month + '_' + start_date + '-' + end_date + '_' + 'Anomaly.png';

    #Add title and save figures
    plt.title(title_str,fontsize=13);
    plt.savefig(name_str,dpi=200,bbox_inches='tight');
    plt.close();
