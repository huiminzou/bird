# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 12:02:29 2018

@author: huimin
"""

import numpy as np
import matplotlib.pyplot as plt


dataset = np.genfromtxt('for_kevin_ferry_sample.csv',dtype=None,names=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','lat','lon'],delimiter=',',skip_header=1)
fig=plt.figure(figsize=(10,8))
plt.subplots_adjust(wspace=0.1,hspace=0.1)
FNCL='necscoast_worldvec.dat'
CL=np.genfromtxt(FNCL,names=['lon','lat'])
ax=fig.add_subplot(1,1,1)
ax.plot(CL['lon'],CL['lat'])

for i in np.arange(1,len(dataset['lat'])):
    ax.plot([dataset['lon'][i-1],dataset['lon'][i]],[dataset['lat'][i-1],dataset['lat'][i]],color='red')
ax.axis([-71.1,-69.9,41.7,42.4])   
plt.savefig('ferry_route',dpi=200)
plt.show()