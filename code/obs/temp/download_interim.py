''' 
This file downloads ERA-Interim temperature data for a particular time period of the year.
Each year is saved as a different file. The data is downloaded in NetCDF format. 
This version is set to download November data for the years 1998-2015, but can be modified under the 'Specify' heading.
BEFORE UPLOADING, MAKE SURE GRID SIZE IS CORRECT. MAY WANT TO MAKE OTHER CHANGES
'''
##-------------------------SPECIFY---------------------------
# Specify the time period for which to download
years = ["1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012",  "2013", "2014", "2015", "2016"] # this should be a list of all the years you would like to download
start_date = "10-31" # the start date for the time period, in format "MM-DD"
end_date ="12-01" # the end date for the time period, in format "MM-DD"
#this is the file where your data will end up. Note that it will be made later
dest_dir = '../../../data/obs/temp/'
#This is the area that will be downloaded
area_capture = "35/85/-25/155"


##------------------------DOWNLOAD----------------------------
#Downloading the data. You should not need to edit the code below here. 
from subprocess import call
from ecmwfapi import ECMWFDataServer
call("mkdir -p " + dest_dir, shell=True)
server = ECMWFDataServer()
for i in range(len(years)):
	server.retrieve({
    		"class": "ei",
    		"dataset": "interim",
    		"date": years[i] + "-"+ start_date +"/to/" + years[i]+ "-"+ end_date,
    		"expver": "1",
    		"grid": "1.5/1.5", # this should match the S2S grid
    		"levtype": "sfc",
    		"param": "167.128",
    		"step": "0",
    		"stream": "oper",
    		"time": "00:00:00/06:00:00/12:00:00/18:00:00",
    		"type": "an",
    		"format": "netcdf",
    		"target": dest_dir +"interim_temp_6hr_"+years[i]+".nc",
    		"area": area_capture,
})
