# -*- coding: utf-8 -*-
"""
Created on Thu May  3 16:10:41 2018

@author: huimin
"""


import numpy as np
import matplotlib.pyplot as plt
date='20170831-25'

FN='necscoast_worldvec.dat'
CL=np.genfromtxt(FN,names=['lon','lat'])
fig,ax=plt.subplots(1,1,figsize=(8,8))#sharex=True,sharey=True,dpi=800,figsize=(15,15))
plt.subplots_adjust(wspace=0.1,hspace=0.1)
ax.plot(CL['lon'],CL['lat'],'b-')
  
filepath='files_20170831_back_7days/'     
lons=np.load(filepath+'lonmassbay.npy')
lats=np.load(filepath+'latmassbay.npy')
times=np.load(filepath+'timemassbay.npy')

for i in range(len(lons)):
    ax.scatter(lons[i][0],lats[i][0],color='green')
    ax.scatter(lons[i][-28],lats[i][-28],color='red')
    ax.plot(lons[i][:-27],lats[i][:-27],'y-')

ax.scatter(lons[i][0],lats[i][0],color='green',label='start')
ax.scatter(lons[i][-27],lats[i][-27],color='red',label='end')
ax.legend(scatterpoints=1)    
ax.set_xlim([-70.3,-69.4])
ax.set_ylim([41.2,41.9])
ax.set_title('AUG_25-31_2017 surface backward particle trajectories(MASSBAY)',fontsize=14)
plt.savefig('backward_particle_tracking_massbay'+date,dpi=200)
plt.show()