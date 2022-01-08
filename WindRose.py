
#Extracting velocity components data from a netCDF data file for all days of every month in 2020 and drawing windrose for every month
#Data is from ERA5, Monthly average Reanalysis, 10m u-component of wind & 10m v-component of wind

from matplotlib import pyplot as plt
import matplotlib.cm as cm
from math import pi
from windrose import WindroseAxes
import math
from netCDF4 import num2date
import cftime
import netCDF4
import numpy as np
import pandas as pd
from netCDF4 import Dataset

f = Dataset ('/home/lida/Desktop/OUREH/12month2020/oure.nc')

uten = f.variables['u10']
vten = f.variables['v10']
time = f.variables ['time']
latitudes = f.variables ['latitude']
longitudes = f.variables ['longitude']
#print(latitudes[1], longitudes[0])
time = num2date (time[:], units=time.units)

def domain_bounderies(year, month, day, lat1, lon1):
    

    latitude = latitudes[:] == lat1
    times = time[:] == cftime.DatetimeGregorian(year,month,day)
    
    l = len(times)
       
    longitude = longitudes[:] == lon1

    times_grid, latitudes_grid, longitudes_grid = [x.flatten() for x in np.meshgrid(time[times], latitudes[latitude], longitudes[longitude], indexing='ij')]
    

    vtenv = vten[times,latitude,longitude].flatten()
    
    utenu = uten[times,latitude,longitude].flatten()
    
    ws = math.sqrt(utenu**2 + vtenv**2)
    
    # calculate meteorological angles from U & V to draw windrose
    
    if vtenv > 0:
       if utenu > 0:
           wd = 90 - math.atan(vten[times,latitude,longitude].flatten()/ uten[times,latitude,longitude].flatten())*180/math.pi   
    
       else:
           wd = abs(math.atan(vten[times,latitude,longitude].flatten()/ uten[times,latitude,longitude].flatten())*180/math.pi) + 270
    
    else:
        if utenu > 0: 
            wd = abs(math.atan(vten[times,latitude,longitude].flatten()/ uten[times,latitude,longitude].flatten())*180/math.pi) + 90
        else:
            wd = 270 - (math.atan(vten[times,latitude,longitude].flatten()/ uten[times,latitude,longitude].flatten())*180/math.pi)
             
  
    df = pd.DataFrame({'time':times_grid, 'uten': utenu, 'vten':vtenv, 'speed': ws, 'direction' : wd})

    
    return df

for month in range (1,13):     # 12 months in range (1,13) 
    latlon_value = domain_bounderies(2020,month,1, 33.5, 51.8)    
    for day in range(2,29):
        
        daily = domain_bounderies(2020,month,day,33.5, 51.8)
        
        latlon_value = latlon_value.append(daily)

    '''# Having data in csv format:
    latlon_value.to_csv('/home/lida/Desktop/OUREH/12month2020/atan/'+ str(month) + 'csv', index=False) 
    #or
    latlon_value.to_excel('/home/lida/Desktop/OUREH/12month2020/atan/'+ str(month) + '.xlsx', index=False)'''
   
    ax = WindroseAxes.from_ax()

    ax.bar(latlon_value.direction, latlon_value.speed, normed = True, opening=0.8, edgecolor='white')
    ax.set_legend()

    fname='/home/lida/Desktop/OUREH/12month2020/NewAngle/' + str(month) +'.png'
    plt.savefig(fname,format='png',dpi=300)

