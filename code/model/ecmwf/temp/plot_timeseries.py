import os

import numpy

import netCDF4

import matplotlib.pyplot as plt





def plot_fig(trmm_anomaly,ec_anomaly,target_week,start_year,end_year,lat,lon,lat_down,lat_up,lon_left,lon_right,title_str,name_str):

    


#Put ECMWF and ECMWF for domain and week selected into list
    
    trmm_anomaly_list = []
    
    for i_year in range(0,trmm_anomaly.shape[1]):
        
	      trmm_anomaly_list.append(numpy.mean(trmm_anomaly[target_week,i_year,:,:]))
    
    
    ec_anomaly_list = []
    
    for i_step in range(0,ec_anomaly.shape[0]):
        
	      for i_year in range(0,ec_anomaly.shape[2]):
            

	         ec_anomaly_list.append(numpy.mean(ec_anomaly[i_step,target_week,i_year,:,:]))
    
    


	#Plot time series
    
    fig,ax = plt.subplots(figsize=(10,5))
    
    xx = range(start_year,end_year+1)
    
    ax.plot([start_year, end_year], [ 0,0], 'k' )
    ax.plot(xx,trmm_anomaly_list,'--bo',linewidth=2,label='ERA-I')
    
    ax.plot(xx,ec_anomaly_list[0:end_year-start_year+1],linewidth=2,label='EC_LT1')
    
    ax.plot(xx,ec_anomaly_list[end_year-start_year+1:(end_year-start_year+1)*2],linewidth=2,label='EC_LT2')
    ax.plot(xx,ec_anomaly_list[(end_year-start_year+1)*2:(end_year-start_year+1)*3],linewidth=2,label='EC_LT3')
    ax.plot(xx,ec_anomaly_list[(end_year-start_year+1)*3:(end_year-start_year+1)*4],linewidth=2,label='EC_LT4')
    #Add title and save figures
    
    plt.legend(loc='best')
    
    plt.title(title_str,fontsize=13)
    
    plt.savefig(name_str,dpi=200,bbox_inches='tight')
    
    plt.close()
