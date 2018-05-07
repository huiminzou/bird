# -*- coding: utf-8 -*-
"""
Created on Mon May  7 14:25:50 2018

@author: huimin
"""

import datetime as dt
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
def sh_bindata(x, y, z, xbins, ybins):
    """
    Bin irregularly spaced data on a rectangular grid.

    """
    ix=np.digitize(x,xbins)
    iy=np.digitize(y,ybins)
    xb=0.5*(xbins[:-1]+xbins[1:]) # bin x centers
    yb=0.5*(ybins[:-1]+ybins[1:]) # bin y centers
    zb_mean=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_median=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_std=np.empty((len(xbins)-1,len(ybins)-1),dtype=z.dtype)
    zb_num=np.zeros((len(xbins)-1,len(ybins)-1),dtype=int)    
    for iix in range(1,len(xbins)):
        for iiy in range(1,len(ybins)):
#            k=np.where((ix==iix) and (iy==iiy)) # wrong syntax
            k,=np.where((ix==iix) & (iy==iiy))
            zb_mean[iix-1,iiy-1]=np.mean(z[k])
            zb_median[iix-1,iiy-1]=np.median(z[k])
            zb_std[iix-1,iiy-1]=np.std(z[k])
            zb_num[iix-1,iiy-1]=len(z[k])
            
    return xb,yb,zb_mean,zb_median,zb_std,zb_num

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
######## Hard codes ##########
data = np.genfromtxt('Copy of GRSH_locations_082017.csv',dtype=None,names=['num','date','lat','lon'],delimiter=',',skip_header=1)    
Model='massbay'
days=0.25
filepath='files_201708_back_7days_differ_starttime/' 
#start_time=dt.datetime(2017,8,31,12,0,0,0)
#end_time =start_time-timedelta(hours=days*24)
FNCL='necscoast_worldvec.dat'
fig,ax=plt.subplots(1,1,figsize=(10,8))
CL=np.genfromtxt(FNCL,names=['lon','lat'])
ax.plot(CL['lon'],CL['lat'],'b-',linewidth=0.5)
#lat=[]
#lon=[]
dates=[]
for i in range(len(data['lon'])):#convert the format to degree
    lat,lon=dm2dd(data['lat'][i],data['lon'][i])
    day=data['date'][i][0:2]
    start_time=dt.datetime(2017,8,int(day),12,0,0,0)
    end_time =start_time-timedelta(hours=days*24)
    ax.scatter(lon,lat,marker='o',color='green',s=8)#plot startpoint
    url_time='http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_MASS_BAY/2017/mbn_201708.nc?time[0:1:743]'
    ds = Dataset(url_time,'r').variables
    
    index1=(start_time-datetime(1858,11,17,00,00,00)).days+(start_time-datetime(1858,11,17,00,00,00)).seconds/(60*60*24)
    index2=(end_time-datetime(1858,11,17,00,00,00)).days+(end_time-datetime(1858,11,17,00,00,00)).seconds/(60*60*24)
    ind1=np.argmin(abs(np.array(ds['time'])-index1))
    ind2=np.argmin(abs(np.array(ds['time'])-index2))
    
    lon_model=np.load('lonc.npy')#massbay model grid point
    lat_model=np.load('latc.npy')#massbay model grid point
    
    #############################################
    urlroms = '''/home/hxu/huiminzou/from xiaojian/massbay/current_08hind_hourly.nc'''#to tell if the point reach to beach
    dsroms = Dataset(urlroms,'r').variables
    
    url1roms = '''/home/hxu/huiminzou/from xiaojian/massbay/gom6-grid.nc'''
    ds1roms = Dataset(url1roms,'r').variables
    lon_u=np.hstack(ds1roms['lon_u'][:])
    lat_u=np.hstack(ds1roms['lat_u'][:])
    lon_v=np.hstack(ds1roms['lon_v'][:])
    lat_v=np.hstack(ds1roms['lat_v'][:])
    
    ##############################################3
    url1='''http://www.smast.umassd.edu:8080/thredds/dodsC/models/fvcom/NECOFS/Archive/NECOFS_MASS_BAY/2017/mbn_201708.nc?u[{0}:1:{1}][0][0:1:165094],v[{0}:1:{1}][0][0:1:165094]'''
    url1 = url1.format(ind2, ind1)
    ds1 = Dataset(url1,'r').variables
    #########################################################
    lonmassbay=[]
    latmassbay=[]
    timemassbay=[]
    
    d=[]
    for b in np.arange(len(lon_model)):
        d.append((lon-lon_model[b])*(lon-lon_model[b])+(lat-lat_model[b])*(lat-lat_model[b]))
    index3=np.argmin(d)
    print 'index3',index3
    temlon=lon
    temlat=lat
    lonmass=[]
    latmass=[]
    timemass=[]

    for c in np.arange(-1,-days*24-1,-1):        
        u_t=ds1['u'][c][0][index3]       
        v_t=ds1['v'][c][0][index3]
        print 'u_t:',u_t,'v_t:',v_t
        
        #print 'a',a,'c',c,'time',start_time-timedelta(days=c/24.0),u_t,v_t
      
        dx = -60*60*u_t; dy = -60*60*v_t#using minus speed to backtrack
        print 'dx:',dx,'dy',dy
        temlon = temlon + (dx/(111111*np.cos(temlat*np.pi/180)))
        temlat = temlat + dy/111111
        #######################################################
        d1=[]
        for dd in np.arange(len(lon_u)): 
            d1.append((lon_u[dd]-temlon)*(lon_u[dd]-temlon)+(lat_u[dd]-temlat)*(lat_u[dd]-temlat))
        index2roms=np.argmin(d1)
        
        d2=[]
        for b1 in np.arange(len(lon_v)): 
            d2.append((lon_v[b1]-temlon)*(lon_v[b1]-temlon)+(lat_v[b1]-temlat)*(lat_v[b1]-temlat))
        index3roms=np.argmin(d2)
        
        v0=np.hstack(dsroms['v'][0][-1][:][:])
        u0=np.hstack(dsroms['u'][0][-1][:][:])
        if v0[index3roms]>100000000 or u0[index2roms]>10000000000:#tell if the point reach to beach
            print 'next'
            dis_coast=[]#all distances to coastline
            for i in range(len(CL)):
                dis=(temlon-CL['lon'][i])**2+(temlat-CL['lat'][i])**2
                dis_coast.append(dis)
            index_nearest=np.argmin(dis_coast)
            lonmass.append(CL['lon'][index_nearest])
            latmass.append(CL['lat'][index_nearest])
            timemass.append(start_time-timedelta(days=c/24.0))
            break
        else:
            lonmass.append(temlon)
            latmass.append(temlat)
            timemass.append(start_time-timedelta(days=c/24.0))
            
    np.save(filepath+'lon%s'%str(i),lonmass)
    np.save(filepath+'lat%s'%str(i),latmass)
    np.save(filepath+'time%s'%str(i),timemass)
    lonmassbay.append(lonmass)
    latmassbay.append(latmass)
    timemassbay.append(timemass)

ax.axis([-70.3,-69.4,41.5,41.9]) 
