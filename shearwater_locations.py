# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 11:22:48 2018

@author: huimin
"""


import numpy as np
import matplotlib.pyplot as plt


dataset = np.genfromtxt('Copy of GRSH_locations_082017.csv',dtype=None,names=['num_birds','date','lat','lon'],delimiter=',',skip_header=1)
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
    
ax.axis([-70.3,-69.4,41.5,41.9])

for a in np.arange(len(dataset['num_birds'])):
    lat,lon=dm2dd(dataset['lat'][a],dataset['lon'][a])
    print 'lat',lat
    print 'lon',lon
    ax.scatter(lon,lat,s=dataset['num_birds'][a]*2,color='red')
ax.plot(CL['lon'],CL['lat'])
plt.suptitle('shearwater_locations',fontsize=15)
plt.savefig('shearwater_locations',dpi=100,bbox_inches="tight")