#This self-defined function is used for visualization.

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def plot_figure(data,start_year,end_year,start_date_list,end_date_list,month,index):

    #Control both figure and axis
    fig,ax = plt.subplots(figsize=(15,5));

    #Match the number of colors with that of model initial dates
    color_index = ['blue','green','red','orange','cyan','magenta','maroon'];

    #Plotting
    for i in range(0,len(data)):
        ax.plot(data[i],linewidth=2,linestyle='-',color=color_index[i],label=start_date_list[i]+'-'+end_date_list[i]);

    #Add years to x axis
    xticks = range(0,end_year-start_year+1);
    ax.set_xticks(xticks);
    xticklabels = [];
    for i_year in range(start_year,end_year+1):
        xticklabels.append(str(i_year))
    ax.set_xticklabels(xticklabels);

    #Define fontsize and label for x and y axis
    ax.tick_params(axis='x',labelsize=15);
    ax.tick_params(axis='y',labelsize=15);
    ax.set_xlabel('Year',fontsize=16);
    if index == 'average':
       ylabel = 'Rainfall Average (mm/day)';
    if index == 'anomaly':
       ylabel = 'Rainfall Anomaly (mm/day)';
    ax.set_ylabel(ylabel,fontsize=16);

    #Plot zero horizontal line for anomaly
    if index == 'anomaly':
       plt.axhline(0,linewidth=2,linestyle='--',color='k');

    #Add legend
    plt.legend(loc=(1.01,0.45),fontsize=15);

    #Define name convention
    if index == 'average':
       name_str = 'TRMM_' + month + '_Rainfall_Average_Time_Series.png';
    if index == 'anomaly':
       name_str = 'TRMM_' + month + '_Rainfall_Anomaly_Time_Series.png';

    #Save figures
    plt.savefig(name_str,dpi=200,bbox_inches='tight');
    plt.close();
