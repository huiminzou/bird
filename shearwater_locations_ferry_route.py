# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:16:42 2018
To run this program,you need these input file:
1.'Copy of GRSH_locations_082017.csv'
2.'for_kevin_ferry_sample.csv'
3.'necscoast_worldvec.dat'(find in this links: https://github.com/xiaojianliu/cape-cod-bay-last-two-picture-new/blob/master/necscoast_worldvec.dat

@author: huimin
"""

import numpy as np
import matplotlib.pyplot as plt


dataset_loc = np.genfromtxt('Copy of GRSH_locations_082017.csv',dtype=None,names=['num_birds','date','lat','lon'],delimiter=',',skip_header=1)
dataset_ferry = np.genfromtxt('for_kevin_ferry_sample.csv',dtype=None,names=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','lat','lon'],delimiter=',',skip_header=1)
fig=plt.figure(figsize=(10,8))
plt.subplots_adjust(wspace=0.1,hspace=0.1)
FNCL='necscoast_worldvec.dat'
CL=np.genfromtxt(FNCL,names=['lon','lat'])
ax=fig.add_subplot(1,1,1)
def dm2dd(lat,lon):
    """
    convert lat, lon from decimal degrees,minutes to decimal degrees
    """
    (a,b)=divmod(float(lat),10000.)   
    aa=int(a)
    bb=float(b)
    (bba,bbb)=divmod(bb,100.)
    bbaa=int(bba)
    bbbb=float(bbb)
    lat_value=aa+bbaa/60.+bbbb/3600.

    if float(lon)<0:
        (c,d)=divmod(abs(float(lon)),10000.)
        cc=int(c)
        dd=float(d)
        (ddc,ddd)=divmod(dd,100.)
        ddcc=int(ddc)
        dddd=float(ddd)
        lon_value=cc+(ddcc/60.)+dddd/3600.
        lon_value=-lon_value
    else:
        (c,d)=divmod(float(lon),10000.)
        cc=int(c)
        dd=float(d)
        (ddc,ddd)=divmod(dd,100.)
        ddcc=int(ddc)
        dddd=float(ddd)
        lon_value=cc+(ddcc/60.)+dddd/3600.
    return lat_value, -lon_value
    
ax.axis([-71.1,-69.4,41.5,42.4])
#######################plot the locations#######################
for a in np.arange(len(dataset_loc['num_birds'])):
    lat,lon=dm2dd(dataset_loc['lat'][a],dataset_loc['lon'][a])
    ax.scatter(lon,lat,s=dataset_loc['num_birds'][a]*2,color='red')
#########################plot ferry route######################
for i in np.arange(1,len(dataset_ferry['lat'])):
    ax.plot([dataset_ferry['lon'][i-1],dataset_ferry['lon'][i]],[dataset_ferry['lat'][i-1],dataset_ferry['lat'][i]],color='red')
ax.plot(CL['lon'],CL['lat'])
plt.suptitle('shearwater_locations & ferry route',fontsize=15)
plt.savefig('shearwater_locations_ferry_route',dpi=100,bbox_inches="tight")
