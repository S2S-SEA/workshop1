#This self-defined function is used for visualization.

import matplotlib as mpl
mpl.use('Agg')
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def plot_figure(data_0,lat_0,lon_0,month,step):

    #Caculate borders for the domain
    latcorners = [lat_0.min(),lat_0.max()];
    loncorners = [lon_0.min(),lon_0.max()];

    #Add basemap
    m = Basemap(projection='merc',llcrnrlon=loncorners[0],llcrnrlat=latcorners[0],urcrnrlon=loncorners[1],urcrnrlat=latcorners[1],resolution='h',area_thresh=10);
    m.drawmapboundary();
    m.drawcoastlines();
    m.drawcountries();

    #Draw parallels and meridians
    parallels = np.arange(-20.,30.,10.);
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=12);
    meridians = np.arange(80.,150.,10.);
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=12);

    #Compute map proj coordinates
    data = data_0[::-1];
    ny = data.shape[0]; 
    nx = data.shape[1];
    lons,lats = m.makegrid(nx,ny);
    x,y = m(lons,lats);

    #Define discrete colormap
    cmap = mpl.colors.ListedColormap([(0.7451,0.8627,1),(0.9216,0.9216,0.9216),(1,0.9804,0.4902),(1,0.8235,0.8235),(1,0.6863,0.6863),(1,0.4902,0.4902),(1,0.1529,0.1529),(0.8235,0,0),(0.5961,0,0),(0.4510,0,0),(0.2941,0,0)]);
    bounds = [-1.,0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.];
    norm = mpl.colors.BoundaryNorm(bounds,cmap.N);

    #Plotting
    cs = m.pcolormesh(x,y,data,cmap=cmap,norm=norm);

    #Add colorbar
    cbar = m.colorbar(cs,location='bottom',pad="5%");
    cbar.set_ticks([0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.]);
    cbar.set_ticklabels(['0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1']);

    #Define title and name convention
    title_str = 'Rainfall CORA' + ' (' + 'LT+' + step + ')';
    name_str = 'ECMWF_' + month + '_' + 'LT-' + step + '_CORA.png';

    #Add title and save figures
    plt.title(title_str,fontsize=13);
    plt.savefig(name_str,dpi=200,bbox_inches='tight');
    plt.close();
